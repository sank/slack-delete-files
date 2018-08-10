import requests
import datetime
import time
import calendar


def date_to_unixtime(dt):
    """
    Convert python datetime to Unix timestamp
    :param dt: python datetime
    :return: Unix time
    """
    return int(calendar.timegm(dt.timetuple()))


# Create slack token at https://api.slack.com/custom-integrations/legacy-tokens
SLACK_TOKEN = 'xoxp-***********-**********-***********-*****************************'
# Specify until which date to delete the goods
DATE_TO = datetime.datetime(2018, 7, 3, 16, 23, 29)

date_to = date_to_unixtime(DATE_TO)
url = 'https://slack.com/api/files.list'
url_del = 'https://slack.com/api/files.delete'
r = requests.get(url, params={'token': SLACK_TOKEN, 'ts_to': date_to})
last_page = r.json()['paging']['pages']

for i in range(last_page):
    r = requests.get(url, params={'token': SLACK_TOKEN, 'page': i+1, 'ts_to': date_to})
    if r.status_code != 200:
        print('Error: %s' % r.text)
        break
    else:
        f = r.json()
        for f in f['files']:
            r = requests.post(url_del, params={'token': SLACK_TOKEN, 'file': f['id']})
            if r.status_code != 200:
                print('Error: %s' % r.text)
                break
        print('page %s ok' % (i+1))
    # TODO: On last iteration do not need to do this:
    time.sleep(60)

