class TimedEventSystem(object):
    def __init__(self):
        self._events = []

    def add(self, delay, func):
        evt = self._TimedEvent(self, delay, func)
        self._events.append(evt)
        return evt

    def remove(self, event):
        self._events.remove(event)

    def update(self, delta):
        for event in self._events:
            event.update(delta)
    
    class _TimedEvent(object):
        def __init__(self, parent, delay, func):
            self.parent = parent
            self.delay = delay
            self.func = func
            self.elapsed = 0

        def update(self, delta):
            self.elapsed += delta
            if self.elapsed >= self.delay:
                self.func()
                self.kill()

        def kill(self):
            self.parent.remove(self)
