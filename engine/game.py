import pygame
from pygame.locals import *
from inputadapter import KeyboardAdapter, MouseAdapter
import ecs

class Game(object):
    def __init__(self, width, height, **kwargs):
        global instance
        print("Initializing game")
        fullscreen = kwargs.get("fullscreen", False)
        self._frame_rate = kwargs.get("frame_rate", 30)
        pygame.init()
        if fullscreen:
            self._screen = pygame.display.set_mode((width, height),
                                                   FULLSCREEN | HWSURFACE)
        else:
            self._screen = pygame.display.set_mode((width, height),
                                                   HWSURFACE)
        self._screen_rect = pygame.Rect(0, 0, width, height)
        self.window_title = kwargs.get("title", "PyGame Window")
        self.background_color = 0, 0, 0
        self._keyboard = KeyboardAdapter()
        self._mouse = MouseAdapter()
        self._scenes = {}
        self._current_scene = None
        self._next_scene = None
        self._finished = False
        instance = self
        print("Game is ready for scenes")

    def add_scene(self, scene):
        name = scene.name
        self._scenes[name] = scene
        if self._next_scene is None:
            self._next_scene = name
        print("Scene {} has been added to the game".format(name))

    def _load_scene(self, name):
        scene_class = self._scenes[name]
        scene_object = scene_class(self)
        scene_object.parent = self
        return scene_object

    def set_next_scene(self, name):
        scene_class = self._scenes[name]
        if scene_class is None:
            raise Exception("Could not find scene: {}".format(name))
        self._next_scene = name
        print("Set next scene to {}".format(name))

    def start(self):
        if len(self._scenes) == 0:
            raise Exception("cannot start game, there are no scenes")
        else:
            while self._finished is False:
                self.current_scene = self._load_scene(self._next_scene)
                current_scene_name = self.current_scene.name
                print("Initializing scene: {}".format(current_scene_name))
                self.current_scene.on_init()
                print("Beginning game loop")
                clock = pygame.time.Clock()
                while self.current_scene.finished is False: # main loop
                    delta = clock.tick(self._frame_rate)
                    events = self._process_events()
                    self.current_scene.on_update(delta, events)
                    ecs.trigger("Update", delta)
                    self._screen.fill(self.background_color)
                    self.current_scene.on_render(self._screen)
                    ecs.trigger("Render", self._screen)
                    pygame.display.flip()
                print("Cleaning up scene: {}".format(current_scene_name))
                self.current_scene.on_cleanup()
        pygame.quit()
    
    def _process_events(self):
        quit_evt = pygame.event.get(QUIT)
        if quit_evt:
            print("Window manager exit request")
            self.stop()
        keyboard_evts = pygame.event.get([KEYDOWN, KEYUP])
        self.keyboard.update(keyboard_evts)
        mouse_evts = pygame.event.get([MOUSEBUTTONDOWN, MOUSEBUTTONUP,
                                      MOUSEMOTION])
        self.mouse.update(mouse_evts)
        usr_evts = pygame.event.get(USEREVENT)
        return usr_evts

    def stop(self):
        self.current_scene.finished = True
        self._finished = True

    def get_width(self):
        return self._screen_rect.width

    def get_height(self):
        return self._screen_rect.height
    
    @property
    def keyboard(self):
        return self._keyboard
    
    @property
    def mouse(self):
        return self._mouse
    
    @property
    def window_title(self):
        return pygame.display.get_caption()[0]
    
    @window_title.setter
    def window_title(self, string):
        pygame.display.set_caption(string)
    
    @property
    def screen_rect(self):
        return Rect(self._screen_rect)

class Scene(object):
    name = "unnamed"

    def __init__(self, game):
        self.parent = game
        self.finished = False

    def on_init(self):
        raise NotImplementedError("Scene.on_init() is not implemented")

    def on_update(self, delta, events):
        raise NotImplementedError("Scene.on_update() is not implemented")

    def on_render(self, screen):
        raise NotImplementedError("Scene.on_render() is not implemented")

    def on_cleanup(self):
        raise NotImplementedError("Scene.on_cleanup() is not implemented")
