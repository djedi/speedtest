#!/usr/bin/python
import os
import csv
import datetime
import time
import twitter


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


def test():
    # run speedtest-cli
    date = datetime.datetime.now()
    print 'running test'
    speedtest_path = os.popen('which speedtest-cli').read().strip()
    results = os.popen('{} --simple'.format(speedtest_path)).read()
    print 'ran'
    # split the 3 line result (ping,down,up)
    lines = results.split('\n')
    print results
    # if speedtest could not connect set the speeds to 0
    if 'Cannot' in results:
        ping = 100
        down = 0
        up = 0
    # extract the values for ping down and up values
    else:
        """
        Output will look something like:
        Ping: 74.526 ms
        Download: 57.84 Mbit/s
        Upload: 3.49 Mbit/s
        """
        ping = float(lines[0][6:-3])
        down = float(lines[1][10:-7])
        up = float(lines[2][8:-7])

    print date, ping, down, up

    # save the data to file for local network plotting
    out_file = open('data.csv', 'a')
    writer = csv.writer(out_file)
    writer.writerow((date, ping, down, up))
    out_file.close()

    my_auth = twitter.OAuth(
            ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twit = twitter.Twitter(auth=my_auth)

    biz_res = 'Residential'
    biz_rez_hashtag = ''
    if COMCAST_BUSINESS:
        biz_res = 'Comcast Business'
        biz_rez_hashtag = '#comcastbusiness'

    # try to tweet if speedtest couldnt even connet.
    # Probably wont work if the internet is down
    if 'Cannot' in results:
        try:
            tweet = '.@ComcastCares why is my internet down? I pay for ' \
                    '{}down/{}up ({}) in {}. ' \
                    '#comcastoutage #comcast'.format(
                        DOWNLOAD_SPEED_PAYING_FOR,
                        UPLOAD_SPEED_PAYING_FOR,
                        biz_res,
                        LOCATION
                    )
            twit.statuses.update(status=tweet)
        except:
            pass

    elif int(down) < TWEET_IF_DOWNLOAD_LESS_THAN:
        print 'trying to tweet'
        try:
            tweet = '.@ComcastCares why is my internet speed {}down/{}up ' \
                    'when I pay for {}down/{}up in {}? #comcast ' \
                    '#speedtest {}'.format(
                        int(down), int(up), DOWNLOAD_SPEED_PAYING_FOR,
                        UPLOAD_SPEED_PAYING_FOR, LOCATION, biz_rez_hashtag)
            twit.statuses.update(status=tweet)
        except Exception, e:
            print str(e)
    elif int(up) < TWEET_IF_UPLOAD_LESS_THAN:
        print 'tweeting upload speed'
        try:
            tweet = '.@ComcastCares why is my upload speed so slow ' \
                    '({} Mbit/s)? I pay for {}down/{}up {} ' \
                    'in {}. #speedtest'.format(
                        int(up),
                        DOWNLOAD_SPEED_PAYING_FOR,
                        UPLOAD_SPEED_PAYING_FOR,
                        biz_res,
                        LOCATION
                    )
            twit.statuses.update(status=tweet)
        except Exception, e:
            print str(e)


if __name__ == '__main__':
    test()
    print 'completed'
