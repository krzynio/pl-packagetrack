#!/usr/bin/env python
import dateparser
import re
import json
import os
import sys
import requests

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from models import trackingStatus, trackingEvent
from exceptions import NotFoundPackage

NAME = "TNT"


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

    if r.status_code == 200:

        data = json.loads(r.text)

        if 'notFound' in data['tracker.output']:
            raise NotFoundPackage()
        else:
            track = data['tracker.output']['consignment'][0]['statusData']

            events = []
            for row in track:
                stage_date = dateparser.parse("{} {}".format(row['localEventDate'], row['localEventTime']), settings={'DATE_ORDER': 'YMD'})
                events.append(trackingEvent(time=stage_date, place=row['depot'], status=row['statusDescription']))

            return trackingStatus(number, 'TNT', 'DONE', events)
