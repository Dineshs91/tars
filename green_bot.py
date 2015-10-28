#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import time

import requests


GREENKEEPER_BOT = 'greenkeeperio-bot'
DEVLOG_BOT = 'devlog-bot'

owner = 'dineshs91'
repo = 'devlog'


def add_log(msg):
    print '[%s]: %s' %(time.asctime(), msg)

# Check if bot has already added a comment
def has_bot_comment(pull_number):
    resp = requests.get('https://api.github.com/repos/%s/%s/issues/%d/comments' %(owner, repo, pull_number))
    json_resp = json.loads(resp.text)

    for comment in json_resp:
        if comment.get('user').get('login') == DEVLOG_BOT:
            return True
    return False

def create_comment(pull_number, message, access_token):
    data = json.dumps({
        'body': message
    })

    headers = {
        'Authorization': 'token %s' %access_token,
    }

    requests.post('https://api.github.com/repos/%s/%s/issues/%d/comments' %(owner, repo, pull_number),
                  data=data,
                  headers=headers)

def merge_pr(pull_number, sha, title):
    # Process title to remove any use of breaks build
    title = title.replace('breaks build 🚨', 'update')

    data = json.dumps({
        'commit_message': title,
        'sha': sha
    })

    headers = {
        'Authorization': 'token %s' %access_token,
    }

    resp = requests.put('https://api.github.com/repos/%s/%s/pulls/%d/merge' %(owner, repo, pull_number), 
                        data=data,
                        headers=headers)
    resp_text = json.loads(resp.text)
    add_log(resp_text)

    # Delay of 3 mins (180 secs)
    time.sleep(180)

def check_and_merge(pull_number, ref, sha, title):
    # Check if CI tests have passed
    status = requests.get('https://api.github.com/repos/%s/%s/commits/%s/status' %(owner, repo, ref))

    stat_content = json.loads(status.text)
    status = stat_content.get('state')
    
    # Check if the current PR is mergeable
    single_pr = requests.get('https://api.github.com/repos/%s/%s/pulls/%d' %(owner, repo, pull_number))

    single_pr_content = json.loads(single_pr.text)
    is_mergeable = single_pr_content.get('mergeable')

    if status == 'success' and not is_mergeable and not has_bot_comment(pull_number):
        create_comment(pull_number, "This PR cannot be merged by me(bot).", access_token)
        return
    elif status == 'success' and is_mergeable:
        merge_pr(pull_number, sha, title)

def main():
    add_log('Job started')

    # Parsing config
    cfg = json.load(open('green.cfg'))
    access_token = cfg.get('access_token')

    if access_token == None:
        add_log('Failed to fetch access token')
        return

    pull_requests = requests.get('https://api.github.com/repos/%s/%s/pulls' %(owner, repo))
    pr_content = json.loads(pull_requests.text)

    if isinstance(pr_content, dict):
        add_log(pull_requests.status_code + pr_content.get('message'))
        return

    for content in pr_content:
        user = content.get('user').get('login')
        pull_number = content.get('number')
        ref = content.get('head').get('ref').encode('utf8')
        sha = content.get('head').get('sha').encode('utf8')
        title = content.get('title').encode('utf8')
    
        if user == GREENKEEPER_BOT:
            check_and_merge(pull_number, ref, sha, title)

    add_log('Job ended')
            
if __name__ == "__main__":
    main()
