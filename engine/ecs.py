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

def create_component(name):
    component = _components.get(name, None)
    if component == None:
        return None
    else:
        return component()

def destroy_all():
    for entity in _entities:
        entity.destroy()

def query(components):
    c_names = components.split(", ")
    c_count = len(c_names)
    if c_count == 0:
        return None
    elif c_count == 1:
        return _relationships[c_names[0]]
    else:
        e_lists = []
        for c_name in c_names:
            e_lists.append(_relationships[c_name])
        l_list = e_lists[1]
        r_list = []
        i = 0
        while i < c_count - 1:
            r_list = e_lists[i + 1]
            new_list = [e for e in l_list if e in r_list]
            l_list = new_list
            i += 1
        return l_list

class Entity(object):
    def __init__(self, components=None):
        self._bindings = {}
        self._components = []
        _entities.append(self)
        if not components == None:
            c_names = components.split(", ")
            for c_name in c_names:
                self.add(c_name)
    
    def destroy(self):
        for component in self._components:
            _relationships[component].remove(self)
        _entities.remove(self)

    def add(self, c_name):
        self._components.append(c_name)
        a_name = "c_{}".format(c_name.lower())
        component = create_component(c_name)
        setattr(self, a_name, component)
        _relationships[c_name].append(self)
        getattr(self, a_name).add_notify(self)
    
    def remove(self, c_name):
        self._components.remove(c_name)
        a_name = "c_{}".format(c_name.lower())
        delattr(self, a_name)
        _relationships[c_name].remove(self)
        
    @property
    def components(self):
        return list(self._components)
    
    def has_component(self, c_name):
        a_name = "c_{}".format(c_name.lower())
        if hasattr(self, a_name):
            return True
        return False
        
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
