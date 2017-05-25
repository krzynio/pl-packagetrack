#!/usr/bin/env python

import requests
import sys, os
from pyquery import PyQuery as pq
import time
import logging
import json
import dateparser
import re

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from models import trackingStatus,trackingEvent

NAME = "InPost"
ID = __name__[10:]
POPULARITY = 9

def guess(number):
    return len(number) == 24

def track(number):
    
    r = requests.get("https://tracking.inpost.pl/api/v1/history/package[0]=%s?_=%d" % (number, time.time()*1000.0), 
                    headers = {
                                'Referer': "https://inpost.pl/pl/pomoc/znajdz-przesylke?parcel=%s" % number,
                                'User-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                                'Origin': "https://inpost.pl"
                                 },
   
                    )
    data = json.loads(r.text)

    try:
        maxstatus = int(data['maxStatusCode'][5:])
    except:
        return trackingStatus(number, ID, 'NOTFOUND', [])
    events = []
    status_ = 'TRANSIT'
       
    for event in range(maxstatus+1):
        if 'index%d' % event in data['history']:
            row = data['history']['index%d' % event]
            office = ''
            if row['pl'].startswith('Przyjęta w oddziale InPost - '):
                office = row['pl'][29:]
                status = row['pl'][0:26]
            else:
                office = ""
                status = row['pl']    
            d = dateparser.parse(row['changeDate'], settings={'DATE_ORDER': 'YMD'})
            print(row)
            events.append(trackingEvent(d, office, status))
            if re.search("Doręczono", status):
                status_ = "DELIVERED"
    
    if len(events) > 0:
        return trackingStatus(number, ID, status_, events[::-1])
    else:
        return trackingStatus(number, ID, 'NOTFOUND', [])
    
