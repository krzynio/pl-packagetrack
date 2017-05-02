#!/usr/bin/env python
import dateparser
import re
import json
import os
import sys
import requests

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from models import trackingStatus, trackingEvent

NAME = "GLS"
ID = __name__[10:]
POPULARITY = 0


def guess(number):
    """Check length of number."""
    return len(number) == 11


def track(number):
    """Request tracking company about package status.

    :param number: package number in tracking company
    :return: Package status
    """

    payload = {
        'match': number
    }

    r = requests.get("https://gls-group.eu/app/service/open/rest/PL/pl/rstt001", params=payload)
    status = 'TRANSIT'

    if r.status_code == 200:

        data = json.loads(r.text)
        if 'lastError' in data:
            return trackingStatus(number, ID, 'NOTFOUND', [])
        else:
            tracking = data['tuStatus'][0]['history']
            events = []
            for row in tracking:
                stage_date = dateparser.parse("{} {}".format(row['date'], row['time']), settings={'DATE_ORDER': 'YMD'})
                events.append(trackingEvent(time=stage_date, place=row['address']['city'], status=row['evtDscr']))
                if re.search("Paczka doreczona", row['evtDscr']):
                    status = "DELIVERED"
            return trackingStatus(number, ID, status, events)
    else:
        return trackingStatus(number, ID, 'NOTFOUND', [])
