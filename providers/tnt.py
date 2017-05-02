#!/usr/bin/env python
import dateparser
import re
import json
import os
import sys
import requests

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from models import trackingStatus, trackingEvent

NAME = "TNT"
ID = __name__[10:]
POPULARITY = 0


def guess(number):
    """Check length of number."""
    return len(number) == 9


def track(number):
    """Request tracking company about package status.

    :param number: package number in tracking company
    :return: Package status
    """

    payload = {
        'con': number,
        'locale': 'pl_PL',
        'searchType': 'CON'
    }

    r = requests.get("https://www.tnt.com/api/v1/shipment", params=payload)
    status = 'TRANSIT'

    if r.status_code == 200:

        data = json.loads(r.text)
        if 'notFound' in data['tracker.output']:
            return trackingStatus(number, ID, 'NOTFOUND', [])
        else:
            tracking = data['tracker.output']['consignment'][0]['statusData']

            events = []
            for row in tracking:
                stage_date = dateparser.parse("{} {}".format(row['localEventDate'], row['localEventTime']), settings={'DATE_ORDER': 'YMD'})
                events.append(trackingEvent(time=stage_date, place=row['depot'], status=row['statusDescription']))
                if re.search("Przesyłka dostarczona", row['statusDescription']):
                    status = "DELIVERED"
            return trackingStatus(number, ID, status, events)
    else:
            return trackingStatus(number, ID, 'NOTFOUND', [])
