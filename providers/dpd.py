#!/usr/bin/env python

import requests
import sys, os
from pyquery import PyQuery as pq
import time
import logging
import dateparser

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from models import trackingStatus,trackingEvent

NAME = "DPD"

OFFICES = {
    'OSZ': 'Koszalin',
    'POZ': 'Komorniki k/Poznania',
    'RYB': 'Rybnik',
    'RZE': 'Głogów Małopolski',
    'SZZ': 'Dołuje',
    'TAR': 'Tarnów',
    'TOR': 'Toruń',
    'WA1': 'Warszawa',
    'WA2': 'Warszawa',
    'WA3': 'Pruszków',
    'WBA': 'Wałbrzych',
    'WRO': 'Wrocław',
    'ZGR': 'Zielona Góra'
}

def track(number):
    
    r = requests.post("https://tracktrace.dpd.com.pl/findPackage", 
                    headers = {
                                'Referer': "https://tracktrace.dpd.com.pl/parcelDetails?p1=%s" % number,
                                'User-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
                                'Origin': "https://tracktrace.dpd.com.pl"
                                 },
   
                    data = {
                                'q': number,
                                'typ': 1
                    }
                    )

    d = pq(r.text)
    table = d('table.table-track')
    events = []
    
    for row in table('tr').items():
        l = [t.text() for t in row('td').items()]
        d = dateparser.parse("%s %s" % (l[0], l[1]), settings={'DATE_ORDER': 'YMD'})
        events.append(trackingEvent(d, OFFICES.get(l[3], l[3]), l[2]))
    
    return trackingStatus(number, 'DPD', 'DONE', events)
    