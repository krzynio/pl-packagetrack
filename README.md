# PL-PackageTrack

PL-PackageTrack is a polish package tracking scraping and parser library written in Python 3

See it in action: https://znajdzpaczke.pl/ and track your packages with Facebook bot.

Work in progress.

Supported providers:

* Inpost (Przesyłka, Paczkomaty)
* Poczta Polska
* DHL
* DPD
* Fedex
* Ups
* TNT
* GLS

Example:

```python
#!/usr/bin/env python
from plpackagetrack import tracking

# Module initialization

tracker = tracking()

# Get list of available providers

providers = tracker.providers()

print ("Available providers:", ', '.join(providers))

# Available providers: dpd, poczta, dhl, inpost, fedex, ups, tnt, gls

t = tracker.track('ups', '1Z3743EE6803254243')
print(t)
print('----------')
print(["%s" % n for n in t.items()])
print('----------------------------------------------------\n\n')

```

