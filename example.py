#!/usr/bin/env python
from plpackagetrack import tracking

# Module initialization

tracker = tracking()

# Get list of available providers

providers = tracker.providers()

print ("Available providers:", ', '.join(providers))

# Available providers: dpd, poczta, dhl, inpost, fedex, ups, tnt

# t = tracker.track('poczta', 'RQ065039102MY')
t = tracker.track('ups', '1Z3743EE6803254243')

print(t)
print('----------')
print(["%s" % n for n in t.items()])
print('----------------------------------------------------\n\n')