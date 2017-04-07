#!/usr/bin/env python
from plpackagetrack import tracking

test = {
    'poczta': 'RQ065039102MY',
    'dhl': '16189726178',
    'dpd': '0000014278741S',
    'inpost': '605500093704359014606748'
}

tracker = tracking()
providers = tracker.providers()

print ("Available providers:", ', '.join(providers))

for provider in test: 
    t = tracker.track(provider,test[provider] )
    print('---- [%s] ----' % provider)
    print(t)
    print('----------')
    print(["%s" % n for n in t.items()])
    print('----------------------------------------------------\n\n')