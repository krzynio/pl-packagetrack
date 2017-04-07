#!/usr/bin/env python

import requests
import os, sys
from pyquery import PyQuery as pq
import time
import logging
import dateparser

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from models import trackingStatus,trackingEvent

NAME = "Poczta Polska"

def track(number):
    
    r = requests.get("http://emonitoring.poczta-polska.pl/")
    
    cookies = r.cookies
    session_id = r.cookies['PHPSESSID']
    
    r = requests.post("http://emonitoring.poczta-polska.pl/wssClient.php",
                    headers = {
                                'Referer': "http://emonitoring.poczta-polska.pl/",
                                'User-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                                 
                                 },
                    data = {
                                'n': number,
                                's': session_id
                    },
                    cookies = cookies
                    )
    
    d = pq(r.text)
    table = d('table#zadarzenia_td')
    events = []
    
    i = 0
    
    for row in table('tr').items():

        if i > 0:
            l = [t.text() for t in row('td').items()]
            if(l):
                d = dateparser.parse(l[1], settings={'DATE_ORDER': 'YMD'})
                events.append(trackingEvent(d, l[2], l[0]))
        i = i + 1

    return trackingStatus(number, 'poczta', 'DONE', events[::-1])

