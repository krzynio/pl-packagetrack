#!/usr/bin/env python
from plpackagetrack import tracking

# Module initialization

tracker = tracking()

# Get list of available providers

providers = tracker.providers()

print ("Available providers:", ', '.join(providers))

# Available providers: dpd, poczta, dhl, inpost

t = tracker.track('poczta', 'RQ065039102MY' )
print(t)
print('----------')
print(["%s" % n for n in t.items()])
print('----------------------------------------------------\n\n')