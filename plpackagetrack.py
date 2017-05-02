#!/usr/bin/env python

import sys

from providers import *


class tracking(object):
    def __init__(self):
        self._providers = {}
        
        for module in sys.modules.keys():
            if module.startswith('providers.'):
                self._providers[module[10:]] = globals()[module[10:]]

    def providers(self):
        return (list(self._providers.keys()))
        
    def track(self, provider, number):
        return (getattr(self._providers[provider], 'track')(number))

    def guess(self, number):
        order = {}
        
        for provider in self._providers.keys():
            if getattr(self._providers[provider], 'guess')(number):
                order[provider] = 10 * getattr(self._providers[provider], 'POPULARITY')
            else:
                order[provider] = getattr(self._providers[provider], 'POPULARITY')
        return sorted(order, key=order.get)[::-1]

    def track_all(self, number):
        for provider in self.guess(number):
            tracked = getattr(self._providers[provider], 'track')(number)
            if tracked.status() != 'NOTFOUND':
                return (tracked)
        return None
