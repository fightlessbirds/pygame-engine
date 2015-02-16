import pygame
from pygame.locals import *
from copy import copy

class KeyboardAdapter(object):
    def __init__(self):
        self._key_state = {}
        self._old_key_state = {}
        self._keystrokes = []
        self._string = ""
    
    def __str__(self):
        return self._string
        
    def update(self, keyboard_evts):
        self._keystrokes = []
        self._string = ""
        self._old_key_state = copy(self._key_state)
        for evt in keyboard_evts:
            if evt.type == KEYDOWN:
                self._key_state[evt.key] = True
                keystroke = Keystroke(evt.key)
                self._keystrokes.append(keystroke)
                self._string += keystroke.ascii
            if evt.type == KEYUP:
                self._key_state[evt.key] = False
    
    def key_down(self, key_code):
        return self._key_state.get(key_code, False)
    
    def key_hit(self, key_code):
        if not self._old_key_state.get(key_code, False):
            return self._key_state.get(key_code, False)
        return False
    
    @property
    def keystrokes(self):
        """Returns a list of keys that were pressed, in the order
        they were pressed since the last call to update()."""
        return copy(self._keystrokes)

class MouseAdapter(object):
    def __init__(self):
        self._pos = (0, 0)
        self._old_pos = (0, 0)
        self._button_state = {}
        self._old_button_state = {}
        self._clicks = []
    
    def update(self, mouse_evts):
        self._old_pos = self._pos
        self._clicks = []
        self._old_button_state = copy(self._button_state)
        for evt in mouse_evts:
            if evt.type == MOUSEMOTION:
                self._pos = evt.pos
            if evt.type == MOUSEBUTTONDOWN:
                button = evt.button
                self._button_state[button] = True
                self._clicks.append(Click(evt.pos, button))
            if evt.type == MOUSEBUTTONUP:
                self._button_state[evt.button] = False
    
    @property
    def pos(self):
        return self._pos
    
    @property
    def x(self):
        return self._pos[0]
    
    @property
    def y(self):
        return self._pos[1]
    
    @property
    def dx(self):
        return self._pos[0] - self._old_pos[0]
    
    @property
    def dy(self):
        return self._pos[1] - self._old_pos[1]
    
    def button_down(self, button_code):
        return self._button_state.get(button_code, False)
    
    def button_hit(self, button_code):
        if not self._old_button_state.get(button_code, False):
            return self._button_state.get(button_code, False)
        return False
    
    @property
    def clicks(self):
        return copy(self._clicks)

class Keystroke(object):
    def __init__(self, value):
        self._value = value
        self._ascii = ""
        if value == K_UP:
            self._name = "cursor up"
        elif value == K_DOWN:
            self._name = "cursor down"
        elif value == K_RIGHT:
            self._name = "cursor right"
        elif value == K_LEFT:
            self._name = "cursor left"
        elif value == K_RSHIFT:
            self._name = "right shift"
        elif value == K_LSHIFT:
            self._name = "left shift"
        elif value == K_RCTRL:
            self._name = "right control"
        elif value == K_LCTRL:
            self._name = "left control"
        elif value == K_RALT:
            self._name = "right alt"
        elif value == K_LALT:
            self._name = "left alt"
        elif value == K_BACKSPACE:
            self._ascii = "\b"
            self._name = "backspace"
        elif value == K_TAB:
            self._ascii = "\t"
            self._name = "tab"
        elif value == K_CLEAR:
            self._name = "clear"
        elif value == K_RETURN:
            self._ascii = "\r"
            self._name = "return"
        elif value == K_PAUSE:
            self._name = "pause"
        elif value == K_ESCAPE:
            self._ascii = "^["
            self._name = "escape"
        elif value == K_SPACE:
            self._ascii = " "
            self._name = "space"
        elif value == K_EXCLAIM:
            self._ascii = "!"
            self._name = "exclamation point"
        elif value == K_QUOTEDBL:
            self._ascii = "\""
            self._name = "double quote"
        elif value == K_HASH:
            self._ascii = "#"
            self._name = "hash"
        elif value == K_DOLLAR:
            self._ascii = "$"
            self._name = "dollar"
        elif value == K_AMPERSAND:
            self._ascii = "&"
            self._name = "ampersand"
        elif value == K_QUOTE:
            self._ascii = "'"
            self._name = "apostrophe"
        elif value == K_LEFTPAREN:
            self._ascii = "("
            self._name = "left parenthesis"
        elif value == K_RIGHTPAREN:
            self._ascii = ")"
            self._name = "right parenthesis"
        elif value == K_ASTERISK:
            self._ascii = "*"
            self._name = "asterisk"
        elif value == K_PLUS:
            self._ascii = "+"
            self._name = "plus"
        elif value == K_COMMA:
            self._ascii = ","
            self._name = "comma"
        elif value == K_MINUS:
            self._value = value
            self._ascii = "-"
            self._name = "minus"
        elif value == K_PERIOD:
            self._ascii = "."
            self._name = "period"
        elif value == K_SLASH:
            self._ascii = "/"
            self._name = "forward slash"
        elif value == K_0:
            self._ascii = "0"
            self._name = "0"
        elif value == K_1:
            self._ascii = "1"
            self._name = "1"
        elif value == K_2:
            self._ascii = "2"
            self._name = "2"
        elif value == K_3:
            self._ascii = "3"
            self._name = "3"
        elif value == K_4:
            self._ascii = "4"
            self._name = "4"
        elif value == K_5:
            self._ascii = "5"
            self._name = "5"
        elif value == K_6:
            self._ascii = "6"
            self._name = "6"
        elif value == K_7:
            self._ascii = "7"
            self._name = "7"
        elif value == K_8:
            self._ascii = "8"
            self._name = "8"
        elif value == K_9:
            self._ascii = "9"
            self._name = "9"
        elif value == K_COLON:
            self._ascii = ":"
            self._name = "colon"
        elif value == K_SEMICOLON:
            self._ascii = ";"
            self._name = "semicolon"
        elif value == K_LESS:
            self._ascii = "<"
            self._name = "less than"
        elif value == K_EQUALS:
            self._ascii = "="
            self._name = "equals"
        elif value == K_GREATER:
            self._ascii = ">"
            self._name = "greater than"
        elif value == K_QUESTION:
            self._ascii = "?"
            self._name = "question mark"
        elif value == K_AT:
            self._ascii = "@"
            self._name = "at"
        elif value == K_LEFTBRACKET:
            self._ascii = "["
            self._name = "left bracket"
        elif value == K_BACKSLASH:
            self._ascii = "\\"
            self._name = "backslash"
        elif value == K_RIGHTBRACKET:
            self._ascii = "]"
            self._name = "right bracket"
        elif value == K_CARET:
            self._ascii = "^"
            self._name = "caret"
        elif value == K_UNDERSCORE:
            self._ascii = "_"
            self._name = "underscore"
        elif value == K_BACKQUOTE:
            self._ascii = "`"
            self._name = "backquote"
        elif value == K_a:
            self._ascii = "a"
            self._name = "a"
        elif value == K_b:
            self._ascii = "b"
            self._name = "b"
        elif value == K_c:
            self._ascii = "c"
            self._name = "c"
        elif value == K_d:
            self._ascii = "d"
            self._name = "d"
        elif value == K_e:
            self._ascii = "e"
            self._name = "e"
        elif value == K_f:
            self._ascii = "f"
            self._name = "f"
        elif value == K_g:
            self._ascii = "g"
            self._name = "g"
        elif value == K_h:
            self._ascii = "h"
            self._name = "h"
        elif value == K_i:
            self._ascii = "i"
            self._name = "i"
        elif value == K_j:
            self._ascii = "j"
            self._name = "j"
        elif value == K_k:
            self._ascii = "k"
            self._name = "k"
        elif value == K_l:
            self._ascii = "l"
            self._name = "l"
        elif value == K_m:
            self._ascii = "m"
            self._name = "m"
        elif value == K_n:
            self._ascii = "n"
            self._name = "n"
        elif value == K_o:
            self._ascii = "o"
            self._name = "o"
        elif value == K_p:
            self._ascii = "p"
            self._name = "p"
        elif value == K_q:
            self._ascii = "q"
            self._name = "q"
        elif value == K_r:
            self._ascii = "r"
            self._name = "r"
        elif value == K_s:
            self._ascii = "s"
            self._name = "s"
        elif value == K_t:
            self._ascii = "t"
            self._name = "t"
        elif value == K_u:
            self._ascii = "u"
            self._name = "u"
        elif value == K_v:
            self._ascii = "v"
            self._name = "v"
        elif value == K_w:
            self._ascii = "w"
            self._name = "w"
        elif value == K_x:
            self._ascii = "x"
            self._name = "x"
        elif value == K_y:
            self._ascii = "y"
            self._name = "y"
        elif value == K_z:
            self._value = value
            self._ascii = "z"
            self._name = "z"
        elif value == K_DELETE:
            self._name = "delete"
        elif value == K_KP0:
            self._ascii = "0"
            self._name = "keypad 0"
        elif value == K_KP1:
            self._ascii = "1"
            self._name = "keypad 1"
        elif value == K_KP2:
            self._ascii = "2"
            self._name = "keypad 2"
        elif value == K_KP3:
            self._ascii = "3"
            self._name = "keypad 3"
        elif value == K_KP4:
            self._ascii = "4"
            self._name = "keypad 4"
        elif value == K_KP5:
            self._ascii = "5"
            self._name = "keypad 5"
        elif value == K_KP6:
            self._ascii = "6"
            self._name = "keypad 6"
        elif value == K_KP7:
            self._ascii = "7"
            self._name = "keypad 7"
        elif value == K_KP8:
            self._ascii = "8"
            self._name = "keypad 8"
        elif value == K_KP9:
            self._ascii = "9"
            self._name = "keypad 9"
        elif value == K_KP_PERIOD:
            self._ascii = "."
            self._name = "keypad period"
        elif value == K_KP_DIVIDE:
            self._ascii = "/"
            self._name = "keypad divide"
        elif value == K_KP_MULTIPLY:
            self._ascii = "*"
            self._name = "keypad multiply"
        elif value == K_KP_MINUS:
            self._ascii = "-"
            self._name = "keypad minus"
        elif value == K_KP_PLUS:
            self._ascii = "+"
            self._name = "keypad plus"
        elif value == K_KP_ENTER:
            self._ascii = "\r"
            self._name = "keypad enter"
        elif value == K_KP_EQUALS:
            self._ascii = "="
            self._name = "keypad equals"
        elif value == K_INSERT:
            self._name = "insert"
        elif value == K_HOME:
            self._name = "home"
        elif value == K_END:
            self._name = "end"
        elif value == K_PAGEUP:
            self._name = "page up"
        elif value == K_PAGEDOWN:
            self._name = "page down"
        elif value == K_F1:
            self._name = "f1"
        elif value == K_F2:
            self._name = "f2"
        elif value == K_F3:
            self._name = "f3"
        elif value == K_F4:
            self._name = "f4"
        elif value == K_F5:
            self._name = "f5"
        elif value == K_F6:
            self._name = "f6"
        elif value == K_F7:
            self._name = "f7"
        elif value == K_F8:
            self._name = "f8"
        elif value == K_F9:
            self._name = "f9"
        elif value == K_F10:
            self._name = "f10"
        elif value == K_F11:
            self._name = "f11"
        elif value == K_F12:
            self._name = "f12"
        elif value == K_NUMLOCK:
            self._name = "number lock"
        elif value == K_CAPSLOCK:
            self._name = "caps lock"
        elif value == K_SCROLLOCK:
            self._name = "scroll lock"
        elif value == K_RMETA:
            self._name = "right meta"
        elif value == K_LMETA:
            self._name = "left meta"
        elif value == K_LSUPER:
            self._name = "left windows key"
        elif value == K_RSUPER:
            self._name = "right windows key"
        elif value == K_MODE:
            self._name = "mode shift"
        elif value == K_HELP:
            self._name = "help"
        elif value == K_PRINT:
            self._name = "print screen"
        elif value == K_SYSREQ:
            self._name = "sysrq"
        elif value == K_BREAK:
            self._name = "break"
        elif value == K_MENU:
            self._name = "menu"
        elif value == K_POWER:
            self._name = "power"
        elif value == K_EURO:
            self._name = "euro"
        else:
            self._name = "unknown"
            
    @property
    def value(self):
        return self._value
    
    @property
    def name(self):
        return self._name
    
    @property
    def ascii(self):
        return self._ascii

class Click(object):
    def __init__(self, pos, button):
        self._pos = pos
        self._button = button
    
    @property
    def x(self):
        return self._pos[0]
    
    @property
    def y(self):
        return self._pos[1]
    
    @property
    def button(self):
        return self._button
