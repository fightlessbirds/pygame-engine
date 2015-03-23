_entities = []
_relationships = {} # {component_name:[entity]}
_components = {} # {component_name:component}
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
    # trigger local bindings
    for entity in _entities:
        if args:
            entity.trigger(event, *args)
        else:
            entity.trigger(event)

def install(component):
    c_name = component.name
    if not c_name in _components:
        _components[c_name] = component
        _relationships[c_name] = []

def get_component(name):
    component = _components.get(name, None)
    if component == None:
        return None
    else:
        return component

def destroy_all():
    for entity in _entities:
        entity.destroy()

def query(components):
    return
    l_components = components.split(", ")
    l_entities = []
#    for component in l_components:
        

class Entity(object):
    def __init__(self, components=None):
        self._bindings = {}
        self._components = []
        _entities.append(self)
        if not components == None:
            c_names = components.split(", ")
            for c_name in c_names:
                component = get_component(c_name)
                self.add(component())
    
    def destroy(self):
        for component in self._components:
            _relationships[component].remove(self)
        _entities.remove(self)

    def add(self, component):
        c_name = component.name
        self._components.append(c_name)
        a_name = "c_{}".format(c_name.lower())
        setattr(self, a_name, component)
        _relationships[c_name].append(self)
        getattr(self, a_name).add_notify(self)
        
    @property
    def components(self):
        return list(self._components)
        
    def bind(self, event, callback):
        callbacks = self._bindings.get(event, None)
        if callbacks == None:
            self._bindings[event] = [callback]
            return
        callbacks.append(callback)

    def unbind(self, event, callback):
        callbacks = self._bindings.get(event, None)
        if callbacks == None:
            return
        try:
            callbacks.remove(callback)
        except:
            pass # callback is not in callbacks

    def trigger(self, event, *args):
        callbacks = self._bindings.get(event, None)
        if callbacks == None:
            return
        for callback in callbacks:
            print("triggering callback")
            if args:
                callback(*args)
            else:
                callback()

class Component(object):
    name = "Unnamed"
    
    def add_notify(self, entity):
        self.parent = entity
        self.on_init()

    def on_init(self): pass
