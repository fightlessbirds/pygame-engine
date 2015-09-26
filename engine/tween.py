"""
Tweening functions for python

Heavily based on caurina Tweener: http://code.google.com/p/tweener/

Released under M.I.T License - see above url
Python version by Ben Harling 2009
Refactored by Jason Gosen 2015
"""

import math

def OUT_EXPO(t, b, c, d):
    return b+c if (t==d) else c * (-2**(-10 * t/d) + 1) + b;

def LINEAR(t, b, c, d):
    return c*t/d + b

def IN_QUAD(t, b, c, d):
    t/=d
    return c*(t)*t + b

def OUT_QUAD(t, b, c, d):
    t/=d
    return -c *(t)*(t-2) + b

def IN_OUT_QUAD(t, b, c, d):
    t/=d/2
    if ((t) < 1): return c/2*t*t + b
    t-=1
    return -c/2 * ((t)*(t-2) - 1) + b

def OUT_IN_QUAD(t, b, c, d): # crashes
    if (t < d/2):
        return OUT_QUAD (t*2, b, c/2, d)
    return IN_QUAD((t*2)-d, b+c/2, c/2)

def IN_CUBIC(t, b, c, d):
    t/=d
    return c*(t)*t*t + b

def OUT_CUBIC(t, b, c, d):
    t=t/d-1
    return c*((t)*t*t + 1) + b

def IN_OUT_CUBIC(t, b, c, d):
    t/=d/2
    if ((t) < 1):
        return c/2*t*t*t + b
    t-=2
    return c/2*((t)*t*t + 2) + b

def OUT_IN_CUBIC(t, b, c, d):
    if (t < d/2): return OUT_CUBIC (t*2, b, c/2, d)
    return IN_CUBIC((t*2)-d, b+c/2, c/2, d)

def IN_QUART(t, b, c, d):
    t/=d
    return c*(t)*t*t*t + b

def OUT_QUART(t, b, c, d):
    t=t/d-1
    return -c * ((t)*t*t*t - 1) + b

def IN_OUT_QUART(t, b, c, d):
    t/=d/2
    if (t < 1):
        return c/2*t*t*t*t + b
    t-=2
    return -c/2 * ((t)*t*t*t - 2) + b

def OUT_ELASTIC(t, b, c, d):
    if (t==0):
        return b
    t/=d
    if t==1:
        return b+c
    p = period = d*.3
    a = amplitude = 1.0
    if a < abs(c):
        a = c
        s = p/4
    else:
        s = p/(2*math.pi) * math.asin (c/a)
    return (a*math.pow(2,-10*t) * math.sin( (t*d-s)*(2*math.pi)/p ) + c + b)

class Tweener(object):
    def __init__(self):
        """Tweener
        This class manages all active tweens, and provides a factory for
        creating and spawning tween motions."""
        self.current_tweens = []
        self.default_tween_type = IN_OUT_QUAD
        self.default_duration = 1.0

    def has_tweens(self):
        return len(self.current_tweens) > 0


    def add_tween(self, obj, **kwargs):
        """ add_tween(object, **kwargs) -> TweenObject or False

        Example:
        tweener.add_tween( my_rocket, throttle=50, set_thrust=400,
                tween_time=5.0, tween_type=tweener.OUT_QUAD )

        You must first specify an object, and at least one property
        or function with a corresponding change value. The tween
        will throw an error if you specify an attribute the object
        does not possess. Also the data types of the change and the
        initial value of the tweened item must match. If you specify
        a 'set' -type function, the tweener will attempt to get the
        starting value by call the corresponding 'get' function on
        the object. If you specify a property, the tweener will read
        the current state as the starting value. You add both
        functions and property changes to the same tween.

        In addition to any properties you specify on the object,
        these keywords do additional setup of the tween.

        tween_time = the duration of the motion
        tween_type = one of the predefined tweening equations or your own function
        complete_func = specify a function to call on completion of the tween
        update_func = specify a function to call every time the tween updates
        delay = specify a delay before starting.
        """
        t_time = kwargs.pop("tween_time") if "tween_time" in kwargs \
                else self.default_duration

        t_type = kwargs.pop("tween_type") if "tween_type" in kwargs \
                else self.default_tween_type

        t_complete_func = kwargs.pop("complete_func") if "complete_func" in kwargs \
                else None

        t_update_func = kwargs.pop("update_func") if "update_func" in kwargs \
                else None

        t_delay = kwargs.pop("delay") if "delay" in kwargs else 0

        tw = Tween(obj, t_time, t_type, t_complete_func, t_update_func,
                t_delay, **kwargs)
        if tw:
            self.current_tweens.append(tw)
        return tw

    def remove_tween(self, tween_obj):
        if self.current_tweens.contains(tween_obj):
            tween_obj.complete = True

    def remove_all_tweens(self):
        self.current_tweens = []
#        for tween in self.current_tweens:
#            tween.complete = True

    def get_tweens_affecting_object(self, obj):
        """Get a list of all tweens acting on the specified object
        Useful for manipulating tweens on the fly"""
        tweens = []
        for t in self.current_tweens:
            if t.target is obj:
                tweens.append(t)
        return tweens

    def remove_tweening_from(self, obj):
        """Stop tweening an object, without completing the motion
        or firing the complete_func"""
        for t in self.current_tweens:
            if t.target is obj:
                t.complete = True

    def update(self, delta):
        # Convert from milliseconds to seconds
        time_since_last_frame = float(delta) / 1000.0
        for t in self.current_tweens:
            if not t.complete:
                t.update(time_since_last_frame)
            else:
                self.current_tweens.remove(t)

class Tween(object):
    def __init__(self, obj, duration, tween_type, complete_func, update_func, delay, **kwargs):
        """Tween object:
        Can be created directly, but much more easily using Tweener.add_tween( ... )
        """
        self.duration = duration
        self.delay = delay
        self.target = obj
        self.tween = tween_type
        self.tweenables = kwargs
        self.delta = 0
        self.complete_func = complete_func
        self.update_func = update_func
        self.complete = False
        self.t_props = []
        self.t_funcs = []
        self.paused = self.delay > 0
        self.decode_arguments()

    def decode_arguments(self):
        """Internal setup procedure to create tweenables and work out
        how to deal with each"""
        if len(self.tweenables) == 0:
            # nothing to do
            print("TWEEN ERROR: No Tweenable properties or functions defined")
            self.complete = True
            return
        for k, v in self.tweenables.items():
            # check that its compatible
            if not hasattr(self.target, k):
                print("TWEEN ERROR: " + str(self.target) + " has no function " + k)
                self.complete = True
                break
            prop = func = False
            start_val = 0
            change = v
            try:
                start_val = self.target.__dict__[k]
                prop = k
                prop_name = k
            except:
                func = getattr(self.target, k)
                func_name = k
            if func:
                try:
                    get_func = getattr(self.target, func_name.replace("set_", "get_"))
                    start_val = get_func()
                except:
                    start_val = change * 0
                tweenable = Tweenable(start_val, change)
                new_func = [k, func, tweenable]
                self.t_funcs.append(new_func)
            if prop:
                tweenable = Tweenable(start_val, change)
                new_prop = [k, prop, tweenable]
                self.t_props.append(new_prop)

    def pause(self, num_seconds=-1):
        """Pause this tween
        do tween.pause(2) to pause for a specific time
        or tween.pause() which pauses indefinitely."""
        self.paused = True
        self.delay = num_seconds

    def resume(self):
        """Resume from pause"""
        if self.paused:
            self.paused = False

    def update(self, ptime):
        """Update this tween with the time since the last frame
        if there is an update function, it is always called
        whether the tween is running or paused"""
        if self.paused:
            if self.delay > 0:
                self.delay = max(0, self.delay - ptime)
                if self.delay == 0:
                    self.paused = False
                    self.delay = -1
                if self.update_func:
                    self.update_func()
            return
        self.delta = min(self.delta + ptime, self.duration)
        if not self.complete:
            for prop_name, prop, tweenable in self.t_props:
                self.target.__dict__[prop] = self.tween(self.delta,
                        tweenable.start_value, tweenable.change, self.duration)
            for func_name, func, tweenable in self.t_funcs:
                func(self.tween(self.delta, tweenable.start_value,
                        tweenable.change, self.duration))
        if self.delta == self.duration:
            self.complete = True
            if self.complete_func:
                self.complete_func()
        if self.update_func:
            self.update_func()

    def get_tweenable(self, name):
        """Return the tweenable values corresponding to the name of the
        original tweening function or property.

        Allows the parameters of tweens to be changed at runtime.
        The parameters can even be tweened themselves!

        eg:

        # the rocket needs to escape!! - we're already moving, but must go faster!
        twn = tweener.get_tweens_affecting_object(my_rocket)[0]
        tweenable = twn.get_tweenable("thruster_power")
        tweener.add_tween(tweenable, change=1000.0, tween_time=0.4, tween_type=tweener.IN_QUAD)
        """
        ret = None
        for n, f, t in self.t_funcs:
            if n == name:
                ret = t
                return ret
        for n, p, t in self.t_props:
            if n == name:
                ret = t
                return ret
        return ret

    def remove(self):
        """Disables and removes this tween
        without calling the complete function."""
        self.complete = True

class Tweenable(object):
    def __init__(self, start, change):
        """Tweenable:
        Holds values for anything that can be tweened
        these are normally only created by Tweens."""
        self.start_value = start
        self.change = change
