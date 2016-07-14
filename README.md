# Speed Test Script

## Requirements

### speedtest-cli
```$ pip install speedtest-cli```

### Python Twitter API
```$ pip install twitter```

## Twitter App

You'll need to set up an app on [apps.twitter.com](https://apps.twitter.com) in order to get your auth tokens.

## Customization

You'll want to customize the following variables:

```
# twitter connection variables
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
# other settings & thresholds (use integer values)
DOWNLOAD_SPEED_PAYING_FOR = 50
UPLOAD_SPEED_PAYING_FOR = 10
TWEET_IF_DOWNLOAD_LESS_THAN = 30
TWEET_IF_UPLOAD_LESS_THAN = 5
LOCATION = 'SLC, UT'
COMCAST_BUSINESS = True
```

You may also want to edit twitter messages. Look for `tweet = '...'` in the code.

# Automating

To run a speedtest hourly for example, just set up a cron job.

```
$ crontab -e

0 * * * * * python /path/to/test.py
```
