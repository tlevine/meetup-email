#!/usr/bin/env python2
import os
from lxml.html import fromstring
from requests import session
from time import sleep
from random import normalvariate
s = session()

SKIP = {
    'http://www.meetup.com/DataKind-NYC/settings/',
    'http://www.meetup.com/nyhackr/settings/',
    'http://www.meetup.com/Hadoop-NYC/settings/',
}

def login():
    s.post('https://secure.meetup.com/login/', {
        'email': os.environ['MEETUP_EMAIL_ADDRESS'],
        'password': os.environ['MEETUP_PASSWORD'],
        'rememberme': 'on',
        'submitButton': 'Log in',
        'returnUri': '',
        'op': 'login',
        'apiAppName': '',
    })
    return s

def unsubscribe(s, meetup_url):
    r = s.get(meetup_url)
    html = fromstring(r.text)
    board_id = html.cssselect('.D_form input')[-2].xpath('@name')[0].split('_')[1]
    s.post(meetup_url, {
        'eventUpd': '1',
        'evRemind': '1',
        'ePhotCom': '1',
        'faceTag': '1',
        'photoCom': '1',
        'memFrnd': '1',
        ('board_' + board_id): board_id,
        'submit': 'submit',
        'submit': 'Submit',
    })
    return s

def main():
    s = login()
    r = s.get('http://www.meetup.com/account/comm/')
    html = fromstring(r.text)
    meetups = html.xpath('//a[text()="Email and notification settings"]/@href')
    for meetup in meetups:
        if meetup in SKIP:
            continue
        try:
            s = unsubscribe(s, meetup)
        except:
            print 'Error at ', meetup
        else:
            sleep(max(0, normalvariate(10, 5)))

if __name__ == '__main__':
    main()
