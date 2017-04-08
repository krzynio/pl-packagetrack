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
        return(list(self._providers.keys()))
        
    def track(self,provider,number):
        return(getattr(self._providers[provider], 'track')(number))
