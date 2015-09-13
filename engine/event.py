_bindings = {} # {event:[callback]}

def bind(event, callback):
    callbacks = _bindings.get(event, None)
    if callbacks == None:
        _bindings[event] = [callback]
        return
    callbacks.append(callback)

def unbind(event, callback):
    callbacks = _bindings.get(event, None)
    if callbacks == None:
        return
    try:
        callbacks.remove(callback)
    except:
        pass # callback is not in callbacks

def trigger(event, *args):
    # tigger global bindings
    callbacks = _bindings.get(event, None)
    if not callbacks == None:
        for callback in callbacks:
            if args:
                callback(*args)
            else:
                callback()

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
