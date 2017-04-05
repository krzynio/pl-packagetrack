#!/usr/bin/env python
import sys
from tracking import get_providers

test = {
    'poczta': 'RQ065039102MY',
    'dhl': '16189726178',
    'dpd': '0000014278741S',
    'inpost': '605500093704359014606748'
}


plugins = get_providers()


for provider in test:
    t = getattr(plugins[provider], 'track')(test[provider])
    print('---- [%s] ----' % provider)
    print(t)
    print('----------')
    print(["%s" % n for n in t.items()])
    print('----------------------------------------------------\n\n')