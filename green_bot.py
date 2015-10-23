#!/usr/bin/python

import os
import json
import time

import requests


GREENKEEPER_BOT = 'greenkeeperio-bot'
ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN')

owner = 'dineshs91'
repo = 'devlog'

def merge_pr(pull_number, sha, title):
    data = json.dumps({
        'commit_message': title,
        'sha': sha
    })

    headers = {
        'Authorization': 'token %s' %ACCESS_TOKEN,
    }
    
    resp = requests.put('https://api.github.com/repos/%s/%s/pulls/%d/merge' %(owner, repo, pull_number), 
                        data=data,
                        headers=headers)
    resp_text = json.loads(resp.text)
    if isinstance(resp_text, dict):
        print resp_text.message
        
    # Delay of 2 mins (120 secs)
    time.sleep(120)

def check_and_merge(pull_number, ref, sha, title):
    status = requests.get('https://api.github.com/repos/%s/%s/commits/%s/status' %(owner, repo, ref))
    
    stat_content = json.loads(status.text)
    status = stat_content.get('state')
    
    if status == 'success':
        merge_pr(pull_number, sha, title)

def main():
    pull_requests = requests.get('https://api.github.com/repos/%s/%s/pulls' %(owner, repo))
    print '[%s] ' %pull_requests.status_code,
    
    pr_content = json.loads(pull_requests.text)
    if isinstance(pr_content, dict):
        print pull_requests.status_code, pr_content.get('message')
        return
    for i in range(len(pr_content)):
        content = pr_content[i]
        user = content.get('user').get('login')
        pull_number = content.get('number')
        ref = content.get('head').get('ref').encode('utf8')
        sha = content.get('head').get('sha').encode('utf8')
        title = content.get('title').encode('utf8')
    
        if user == GREENKEEPER_BOT:
            check_and_merge(pull_number, ref, sha, title)
            
if __name__ == "__main__":
    main()

