## Tars

Tars is a bot which will automatically merge PR's raised by greenkeeper-io if all the tests pass. It is designed
specifically for [devlog](https://github.com/Dineshs91/devlog) project.

Have a file ```tars.cfg``` with the below config in the root directory

```
{
    access_token: "token"
}
```

This access token should be obtained from github.

Tars can be configured to run as a cron job. There is a great site [crontab.guru](http://crontab.guru/) to find 
out a suitable cron schedule expression.

**Inspired** by [bors](https://github.com/graydon/bors)
