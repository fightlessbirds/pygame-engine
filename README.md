PyGame Engine
=============

A simple game engine for use with PyGame. Written for Python 2.7 and PyGame version 1.9.1.

##License

Engine code is licensed under the GPL v3. The tweening module is licensed under the MIT license.

##Documentation

##game Module
The game module contains classes that encapsulate a PyGame application. A Game object is instantiated and then subclasses of Scene are added to it.

###Game Class
The game class is at the heart of the engine. It contains the core game update loop. Scenes classes are aggregated by a Game object and instantiated on-the-fly. Game is composed of objects of the KeyboardAdapter and MouseAdapter classes.

####Attributes

#####background_color
A tuple of three integers ranging 0-255. The colour that will be used for clearing the screen at the beginning of each frame.

####Properties

#####window_title
A string. The title displayed by the window manager.

#####screen_rect
A PyGame Rect object. Read-only. Represents the dimensions of the game window.

#####keyboard
An instance of the KeyboardAdapter class.

#####mouse
An instance of the MouseAdapter class.

####Functions

#####\_\_init\_\_(self, width, height, **kwargs)
Game class contructor. Initializes PyGame and prepares a Game object that will accept Scene subclasses.

> **width** _int_ - Width of the screen in pixels.

> **height** _int_ - Height of the screen in pixels.

> **fullscreen** _bool_ - Whether the game should be in fullscreen mode.

> **frame_rate** _int_ - The maximum frame rate that the game will run at.

> **title** _str_ - The title of the game displayed by the window manager.

#####add_scene(self, scene)
Add a Scene subclass to the Game object.

> **scene** _Scene_ - A subclass of Scene. Note that it will not work with an instance of a Scene subclass. It must be the subclass itself. Game will instantiate the subclass when the scene is loaded.

#####set_next_scene(self, name)
Set the scene that is to be loaded after the current scene is finished. Raises an exception if the scene cannot be found.

> **name** _str_ - The name of the Scene to be loaded. Must be the same as Scene.name.

#####start(self)
Start the game engine. At least one Scene subclass must be added or an exception is raised. If the next scene has not been explicitly set then the first scene that was added is loaded by default.

#####stop(self)
Stop the game engine. Sets the current Scene object as finished. Sets the Game object as finished.

#####get_width(self)
> **return** _int_ - The width of the game window.

#####get_height(self)
> **return** _int_ - The height of the game window.

###Scene Class
The Scene class encapsulates a scene in the game. Every scene has four functions that are called by its parent Game object and must be implemented: on_init, on_update, on_render, and on_cleanup

####Attributes

#####name
A string containing the name of the Scene. The name is used to reference the Scene when it is loaded. The default name is "unnamed" but this should be modified to be unique for every Scene subclass.

#####finished
Bool that specifies if the Scene is finished. It is set to False when the Scene is loaded. A finished Scene will be cleaned up and freed from memory.

#####parent
Game object that composes the Scene subclass.

####Functions

#####\_\_init\_\_(self, game)
Scene class constructor. Sets the parent Game object and initializes the finished attribute to False. Subclasses of Scene should not implement \_\_init\_\_ but instead do any initialization in on_init.

> **game** _Game_ - The parent Game object.

#####on_init(self)
Called before the game enters the update/render loop for this scene.

#####on_update(self, delta, events)
Called once every iteration of the main loop. Game logic lives here.

> **delta** _int_ - Elapsed milliseconds since the last update.

> **events** _[EventType]_ - A list of PyGame user events that occured since the last update.

##event Module

##gui Module

##inputadapter Module

##loader Module
