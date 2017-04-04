#!/usr/bin/env python

import sys

from providers import *

def get_providers():
    plugins = {}

    for module in sys.modules.keys():
        if module.startswith('providers.'):
            plugins[module[10:]] = globals()[module[10:]]
    return(plugins)
        
    

    