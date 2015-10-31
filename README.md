## Tars

Tars is a bot which will automatically merge PR's raised by greenkeeper-io if all the tests pass. 

Have a file ```tars.cfg``` with the below config.

```
{
    access_token: "token"
}
```

This access token should be obtained from github.

Tars can be configured to run as a cron job. There is a great site [crontab.guru](http://crontab.guru/) to find 
out a suitable cron schedule expression.
