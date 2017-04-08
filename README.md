# PL-PackageTrack

PL-PackageTrack is a polish package tracking scraping and parser library written in Python 3

Work in progress. Status information isn't parsed now, only the events.

Supported providers:

* Inpost (Przesyłka, Paczkomaty)
* Poczta Polska
* DHL
* DPD
* Fedex

Example:

```python
#!/usr/bin/env python
from plpackagetrack import tracking

# Module initialization

tracker = tracking()

# Get list of available providers

providers = tracker.providers()

print ("Available providers:", ', '.join(providers))

# Available providers: dpd, poczta, dhl, inpost, fedex

t = tracker.track('poczta', 'RQ065039102MY')
print(t)
print('----------')
print(["%s" % n for n in t.items()])
print('----------------------------------------------------\n\n')

```

