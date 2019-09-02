#!/usr/bin/env python
import dateparser
import re
import os
import sys
import requests
from pyquery import PyQuery as pq

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from models import trackingStatus, trackingEvent

NAME = "UPS"
ID = __name__[10:]
POPULARITY = 4

def guess(number):
    return number.startswith('1Z')

def track(number):
    """Request tracking company about package status.

    :param number: package number in tracking company
    :return: Package status
    """

    r = requests.post("https://wwwapps.ups.com/WebTracking/track",
                      data={'trackNums': number,
                            'loc': 'pl_PL',
                            'track.x': 'Monitoruj'
                            }
                      )

    d = pq(r.text)
    table = d('table.dataTable')
    status = 'TRANSIT'
    events = []
    for x, row in enumerate(table('tr').items()):
        if x > 0:

            stage = []
            for t in row('td').items():
                td = t.text()
                td = td.translate({ord(c): None for c in '\n\t\r'})
                td = re.sub(r'\s+', ' ', td)
                stage.append(td)

            stage_date = dateparser.parse("{} {}".format(stage[1], stage[2]), settings={'DATE_ORDER': 'YMD'})
            events.append(trackingEvent(time=stage_date, place=stage[0], status=stage[3]))
            if re.search("Doręczono", stage[3]):
                status = "DELIVERED"
    if len(events) > 0:
        return trackingStatus(number, ID, status, events)
    else:
        return trackingStatus(number, ID, 'NOTFOUND', [])
    
