class trackingStatus(object):
    def __init__(self, number, provider, status, items):
        self._number = number
        self._provider = provider
        self._status = status
        self._items = items
    
    def __str__(self):
        return "[%s] %s - %s\n%s" % (self._status, self._provider, self._number, self._items[0])
    
    def number(self):
        return self._number
    
    def provider(self):
        return self._provider
        
    def status(self):
        return self._status
                
    def items(self):
        return self._items
            
class trackingEvent(object):
    def __init__(self, time, place, status):
        self._time = time
        self._place = place
        self._status = status

    def __str__(self):
        return "[%s] %s - %s" % (self._time, self._place, self._status)
