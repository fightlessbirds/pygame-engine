"""
Copyright (C) 2014-2015  Jason Gosen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from copy import copy
import pygame
from pygame.locals import *
from inputadapter import KeyboardAdapter, MouseAdapter

class Game(object):
    """
    Attributes:
        background_color
        finished
        keyboard
        mouse
        _frame_rate
        _screen
        _screen_rect
        _scenes
        _current_scene
        _next_scene
    
    Properties:
        icon
        window_title
        screen_rect
    
    Functions:
        add_scene(scene)
        set_next_scene(name)
        start()
        stop()
        get_width()
        get_height()
        _load_scene(name)
        _process_events()
    """

    def __init__(self, width, height, **kwargs):
        """Initialize the game module. Creates a display window with the
        specified parameters.
        kwargs:  fullscreen = True|False
                 frame_rate = 123
                 title = "window title"
        """
        print("Initializing game")
        # parse keyword arguments
        fullscreen = kwargs.get("fullscreen", False)
        frame_rate = kwargs.get("frame_rate", 30)
        title = kwargs.get("title", "PyGame Window")
        icon = kwargs.get("icon", None)
        # initialize pygame and the game screen
        pygame.init()
        self._frame_rate = frame_rate
        if fullscreen:
            self._screen = pygame.display.set_mode((width, height),
                    FULLSCREEN | HWSURFACE)
        else:
            self._screen = pygame.display.set_mode((width, height),
                    HWSURFACE)
        # set the screen area rect
        self._screen_rect = pygame.Rect(0, 0, width, height)
        # set the window caption
        self.window_title = title
        # set the window icon
        if icon:
            self.icon = icon
        # set the background colour
        self.background_color = 0, 0, 0
        self.keyboard = KeyboardAdapter()
        self.mouse = MouseAdapter()
        # create the dictionary to store scenes.
        self._scenes = {}
        self._current_scene = None
        self._next_scene = None
        # attribute that controls when the game quits
        self.finished = False
        print("Game is ready for scenes")

    def add_scene(self, scene):
        """Add a scene to the game. If no scene has been added prior then
        this scene will be set as the default startup scene.
        scene - A subclass of Scene with all functions implemented.
        name - The name of the scene."""
        name = scene.name
        # add the scene to the dictionary of scene
        self._scenes[name] = scene
        # if no scenes have been added then make this the next scene
        if self._next_scene is None:
            self._next_scene = name
        print("Scene {} has been added to the game".format(name))

    def _load_scene(self, name):
        """Returns an instance of the specified scene."""
        # get scene from scene dictionary
        scene_class = self._scenes[name]
        # create scene instance
        scene_object = scene_class(self)
        # the scene becomes a child of the game
        scene_object.parent = self
        return scene_object

    def set_next_scene(self, name):
        """Set the next scene.
        name - The name for the scene class which has been added to the game."""
        scene_class = self._scenes[name]
        if scene_class is None:
            raise Exception("Could not find scene: {}".format(name))
        self._next_scene = name
        print("Set next scene to {}".format(name))

    def start(self):
        """Starts the game. Control is not passed back to the calling module
        until the game is finished. The game will not start if no scenes have
        been added. When the game ends PyGame will be shut down."""
        # will quit unless scenes are added
        if len(self._scenes) == 0:
            raise Exception("cannot start game, there are no scenes")
        else:
            # the first scene to be added will be executed by default.
            while self.finished is False:
		    self.current_scene = self._load_scene(self._next_scene)
		    current_scene_name = self.current_scene.name
		    print("Initializing scene: {}".format(current_scene_name))
		    self.current_scene.on_init()
		    print("Beginning game loop")
		    clock = pygame.time.Clock()
		    while self.current_scene.finished is False:   # main game loop
		        delta = clock.tick(self._frame_rate)
		        events = self._process_events()
		        self.current_scene.on_update(delta, events)
		        pygame.draw.rect(self._screen, self.background_color,
		                self._screen_rect)
		        self.current_scene.on_render(self._screen)
		        pygame.display.flip()
		    print("Cleaning up scene: {}".format(current_scene_name))
		    self.current_scene.on_cleanup()
        # shut down pygame
        pygame.quit()
    
    def _process_events(self):
        """Process all events that happened this loop. PyGame keyboard
        and mouse events are processed and the engine state is updated
        accordingly. If a QUIT event is detected then the game will
        terminate. Returns a list of USEREVENT events."""
        quit_evt = pygame.event.get(QUIT)
        if quit_evt:
            print("Window manager exit request")
            self.current_scene.finished = True
            self.finished = True
        keyboard_evts = pygame.event.get([KEYDOWN, KEYUP])
        self.keyboard.update(keyboard_evts)
        mouse_evts = pygame.event.get([MOUSEBUTTONDOWN, MOUSEBUTTONUP,
                                      MOUSEMOTION])
        self.mouse.update(mouse_evts)
        usr_evts = pygame.event.get(USEREVENT)
        return usr_evts

    def stop(self):
        """Stop the game."""
        self.current_scene.finished = True
        self.finished = True

    def get_width(self):
        return self._screen_rect.width

    def get_height(self):
        return self._screen_rect.height
    
    @property
    def window_title(self):
        return pygame.display.get_caption()[0]
    
    @window_title.setter
    def window_title(self, string):
        pygame.display.set_caption(string)
    
    @property
    def icon(self):
        return self.window_icon
    
    @icon.setter
    def icon(self, image):
        self.window_icon = image
        pygame.display.set_icon(image)
    
    @property
    def screen_rect(self):
        return copy(self._screen_rect)

class Scene(object):
    """A simple scene class with functions for init/cleanup and
    update/render loops. Simply override the functions, add an instance
    of the subclass to a game object, and start the game. Be sure to
    override the Scene.name variable to hold the name that the scene
    will be identified by."""
    
    name = "unnamed"

    def __init__(self, game):
        self.parent = game
        self.finished = False

    def on_init(self):
        """Called before the game enters the update/render loop for
        this scene."""
        raise NotImplementedError("Scene.on_init() is not implemented")

    def on_update(self, delta, events):
        """Called once every iteration of the main loop. Game logic lives here.
        Arguments:
            delta - The amount of milliseconds that have passed since the
            last update.
            events - List of PyGame events that occured since last update."""
        raise NotImplementedError("Scene.on_update() is not implemented")

    def on_render(self, screen):
        """Called once every iteration of the main loop. Draw to the screen here.
        Arguments:
            screen - A pygame Surface instance that represents the screen."""
        raise NotImplementedError("Scene.on_render() is not implemented")

    def on_cleanup(self):
        """Cleanup any resources used by this scene."""
        raise NotImplementedError("Scene.on_cleanup() is not implemented")
