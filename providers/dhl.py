#!/usr/bin/env python

import requests
import sys, os
from pyquery import PyQuery as pq
import time
import logging
import dateparser

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from models import trackingStatus,trackingEvent

NAME = "DHL"

def track(number):
    r = requests.get("https://webapps.dhl.com.pl/app/tnt/old_cr_sn.aspx?SN=%s" % number, 
                    headers = {               
                                'User-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                    
                                 },
   
                    )
    d = pq(r.text)
    table = d('table#shipment-details-hdr-table')
    i = 0 
    events = []

    for row in table('tr').items():
        if i > 0:
            l = [t.text() for t in row('td').items()]
            d = dateparser.parse("%s %s" % (l[0], l[1]), settings={'DATE_ORDER': 'DMY'})
            l[1]=d
            events.append(trackingEvent(l[1], l[2], l[3]))
        i = i + 1

    return trackingStatus(number, 'dhl', 'DONE', events[::-1])
