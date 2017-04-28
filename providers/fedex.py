#!/usr/bin/env python
import dateparser
import os
import sys
import requests
from pyquery import PyQuery as pq
import re

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from models import trackingStatus, trackingEvent

NAME = "Fedex"
ID = __name__[10:]
POPULARITY = 1

def guess(number):
    return len(number) == 13

def track(number):
    """Request tracking company about package status.

    :param number: package number in tracking company
    :return: Package status
    """

    r = requests.post("https://poland.fedex.com/domestic-shipping/pub/tracktrace.do",
                      data={'packageId': number})

    d = pq(r.text)
    table = d('table.customContentable').eq(0)
    status = 'TRANSIT'
    events = []

    for row in table('tr').items():
        if row.has_class('customContentTableRowOdd') or row.has_class('customContentTableRowEven'):
            stage = [t.text() for t in row('td').items()]
            stage_date = dateparser.parse("%s" % (stage[0]), settings={'DATE_ORDER': 'YMD'})
            events.append(trackingEvent(time=stage_date, place=stage[2], status=stage[1]))
            if re.search("Kurier doręczył przesyłkę do odbiorcy", stage[1]):
                status = "DELIVERED"
            
    if len(events) > 0:
        return trackingStatus(number, ID, status, events)
    else:
        return trackingStatus(number, ID, 'NOTFOUND', [])
