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
    return calendar.timegm(d.timetuple())

token='xoxp-***********-**********-***********-*****************************'
url = 'https://slack.com/api/files.list'
url_del = 'https://slack.com/api/files.delete'
dt = int(date_to_unixtime(datetime.datetime(2018, 7, 3, 16, 23, 29)) / 1000000)
r = requests.get(url, params={'token': token, 'ts_to': dt})
last_page = r.json()['paging']['pages']

for i in range(last_page):
    r = requests.get(url, params={'token': token, 'page': i+1, 'ts_to': dt})
    if r.status_code != 200:
        print('Error: %s' % r.text)
        break
    else:
        f = r.json()
        for f in f['files']:
            r = requests.post(url_del, params={'token': token, 'file': f['id']})
            if r.status_code != 200:
                print('Error: %s' % r.text)
                break
        print('page %s ok' % (i+1))
    time.sleep(60)

