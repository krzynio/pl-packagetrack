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

NAME = "DHL International"
ID = __name__[10:]
POPULARITY = 9

def guess(number):
    return len(number) == 24

def track(number):
    
    r = requests.get("http://www.dhl.com.pl/shipmentTracking?AWB=%s&countryCode=pl&languageCode=pl" % number)
    data = json.loads(r.text)


    if data.get('errors'):
        return trackingStatus(number, ID, 'NOTFOUND', [])
        

    events = []
    status_ = 'TRANSIT'

    for event in data['results'][0]['checkpoints']:
        d = dateparser.parse("%s %s" % (event['date'], event['time']), settings={'DATE_ORDER': 'DMY'})
        events.append(trackingEvent(d, event['location'].rstrip(), event['description']))
        if re.search("Przesyłka doręczona", event['description'] ): 
            status_ = "DELIVERED"

    if len(events) > 0:
        return trackingStatus(number, ID, status_, events)
    else:
        return trackingStatus(number, ID, 'NOTFOUND', [])

    
