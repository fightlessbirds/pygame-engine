PyGame Engine
=============
A simple game engine for use with PyGame. Written for Python 2.7 and PyGame version 1.9.1.
##License
Engine code is licensed under the GPL v3. The tweening module is licensed under the MIT license.
##Example
	from engine.game import Game, Scene
	
	class MyScene(Scene):
	    name = "myscene"
	
	    def on_init(self):
	        self.green = (0, 255, 0)
	
	    def on_cleanup(self):
	        print("nice and tidy")
	
	    def on_update(self, delta, events):
	        print("beep boop beep")
	
	    def on_render(self, screen):
	        screen.fill(self.green)
	
	game = Game(640, 480)
	game.add_scene(MyScene)
	game.start()
##Documentation
##game Module
The game module contains classes that encapsulate a PyGame application. A Game object is instantiated and then subclasses of Scene are added to it.
####Attributes
#####instance
The most recently created Game object.
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
An instance of the KeyboardAdapter class. Read-only.
#####mouse
An instance of the MouseAdapter class. Read-only.
####Functions
#####\_\_init\_\_(width, height, **kwargs)
Game class contructor. Initializes PyGame and prepares a Game object that will accept Scene subclasses.
> **width** _IntType_ - Width of the screen in pixels.

> **height** _IntType_ - Height of the screen in pixels.

> **fullscreen** _BooleanType_ - Whether the game should be in fullscreen mode.

> **frame_rate** _IntType_ - The maximum frame rate that the game will run at.

> **title** _StringType_ - The title of the game displayed by the window manager.

#####add_scene(scene)
Add a Scene subclass to the Game object.
> **scene** _Scene_ - A subclass of Scene. Note that it will not work with an instance of a Scene subclass. It must be the subclass itself. Game will instantiate the subclass when the scene is loaded.

#####set_next_scene(name)
Set the scene that is to be loaded after the current scene is finished. Raises an exception if the scene cannot be found.
> **name** _StringType_ - The name of the Scene to be loaded. Must be the same as Scene.name.

#####start()
Start the game engine. At least one Scene subclass must be added or an exception is raised. If the next scene has not been explicitly set then the first scene that was added is loaded by default.
#####stop()
Stop the game engine. Sets the current Scene object as finished. Sets the Game object as finished.
#####get_width()
> **return** _IntType_ - The width of the game window.

#####get_height()
> **return** _IntType_ - The height of the game window.

###Scene Class
The Scene class encapsulates a scene in the game. Every scene has four functions that are called by its parent Game object and must be implemented: on_init, on_update, on_render, and on_cleanup.
####Attributes
#####name
A string containing the name of the Scene. The name is used to reference the Scene when it is loaded. The default name is "unnamed" but this should be modified to be unique for every Scene subclass.
#####finished
Bool that specifies if the Scene is finished. It is set to False when the Scene is loaded. A finished Scene will be cleaned up and freed from memory.
#####parent
Game object that composes the Scene subclass.
####Functions
#####on_init()
Called before the game enters the update/render loop for this scene.
#####on_update(delta, events)
Called once every iteration of the main loop. Game logic lives here.
> **delta** _IntType_ - Elapsed milliseconds since the last update.

> **events** _[EventType]_ - A list of PyGame user events that occured since the last update.

#####on_render(screen)
Called when it is time to draw the scene to the screen.
> **screen** _Surface_ - The Surface object for the game screen.

#####on_cleanup()
Called after the scene has finished but before it is unloaded.
##event Module
###TimedEventSystem class
This class manages one-shot timed events. Events can be created with a delay and a callback function for when they are finished.
####Functions
#####add(delay, func)
Add a new TimedEvent to the system.
> **delay** _IntType_ - The amount of milliseconds that must pass until the timer runs out.

> **func** _FunctionType_ - The callback function that will be called when the timer runs out.

> **return** _TimedEvent_ - The newly created event object.

#####remove(event)
Remove an event from the system before it has a chance to trigger.
> **event** _TimedEvent_ - The event object ot be removed.

#####update(delta)
Update all TimedEvent objects belonging to this system.
> **delta** _IntType_ - The amount of milliseconds that have elapsed since the last update.

##gui Module
The gui module contains some classes for creating GUI elements that the player can click on.
###ButtonGroup class
A sprite group that manages and updates Button objects. Inherits from the PyGame Group class.
####Functions
#####update(mouse)
Update the button group, checking if any of the buttons have been clicked.
> **mouse** _MouseAdapter_ - The MouseAdapter object to check for clicks.

###Button class
Base class for buttons. Instances are aggregated by the ButtonGroup class.
####Functions
#####update(mouse\_x, mouse_y)
Inherited from the PyGame Sprite class. Called by the parent ButtonGroup.
> **mouse_x** _IntType_ - Mouse position on the x-axis.

> **mouse_y** _IntType_ - Mouse position on the y-axis.

#####on_click()
Called when the button is clicked. Override this to create a callback function for the button.

###TextButton class
A button that appears as text.
####Functions
#####\_\_init\_\_(text, font_size, color=(255, 255, 255))
TextButton class constructor.
> **text** _StringType_ - The text to be displayed on the button.

> **font_size** _IntType_ - The font size used to render the text.

> **color** (_IntType_) - A tuple of three integers ranging 0-255. The colour for the text.

###ImageButton class
A button that appears as an image.
####Functions
#####\_\_init\_\_(image)
ImageButton class constructor. Create a new button that appears as an image.
> **image** _Surface_ - The image to be displayed on the button. A PyGame Surface object.

##inputadapter Module
This module contains classes that make it easy to get input from the player. The input adapter classes are composed by the Game class.
###KeyboardAdapter class
Helper class for getting input from the keyboard.
####Properties
#####keystrokes
A list of Keystroke objects that were spawned since the last update. Read-only.
####Functions
#####update(keyboard_evts)
Update the state of the keyboard adapter. This function should be called once during each iteration of the main game loop.
> **keyboard_evts** _[EventType]_ - List of PyGame event objects related to the keyboard.

#####key\_down(key_code)
Check if a key is being held down.
> **key_code** _IntType_ - The PyGame key code for the key to check.

> **return** _BooleanType_ - True/False if the key is being held down.

#####key\_hit(key_code)
Check if a key has just been pressed since the last update.
> **key_code** _IntType_ - The PyGame key code for the key to check.

> **return** _BooleanType_ - True/False if the key was pressed.

###Keystroke class
This class encapsulates a key being pressed on the keyboard.
####Properties
#####value
Integer representing the PyGame key code. Read-only.
#####name
String human readable name for the key. Read-only.
#####ascii
String ascii representation of the key. Ready-only.
####Functions
#####\_\_init\_\_(value)
Keystroke class constructor.
> **value** _IntType_ - PyGame key code for which key this Keystroke object should represent.

####\_\_str\_\_()
String representation of the KeyboardAdapter object.
> **return** _StringType_ - Returns a string built from the keys that were pressed since the last update.

###MouseAdapter class
Helper class for getting input from the mouse.
####Properties
#####pos
A tuple of integers for the location of the mouse on the x and y-axis. Read-only.
#####x
The location of the mouse on the x-axis. Read-only.
#####y
The location of the mouse on the y-axis. Read-only.
#####dx
Change in position on the x-axis. Read-only.
#####dy
Change in position of the y-axis. Read-only.
#####clicks
A list of Click objects that were spawned since the last update. Read-only.
#####click
The most recent Click object that was spawned since the last update. Read-only.
####Functions
#####update(mouse_evts)
Update the state of the mouse adapter. This function should be called once ever iteration of the main game loop.
> **mouse_evts** _[EventType]_ - A list of PyGame mouse events that occured since the last update.

#####button\_hit(button_code)
#####button\_down(button_code)
###Click class
This class encapsulates a button being pressed on the mouse.
####Properties
#####x
Integer location on the x-axis of the mouse click. Read-only.
#####y
Integer location on the y-axis of the mouse click. Read-only.
#####button
Integer number for the button being pressed. Read-only.
####Functions
#####\_\_init\_\_(pos, button)
Click class contructor.
> **pos** _(IntType)_ - A tuple containing the x and y location where the mouse was clicked.

> **button** _IntType_ - PyGame button code for the button that was pressed.

##loader Module
The loader module contains functions for loading game resources. Resources are cached to save memory and time for when they are loaded again later.
####Functions
#####load(file_name)
Load a resource. The type of resource is determined automatically by the file extention.
> **return** _Surface/Sound_ - The loaded resource.

#####load_image(file_name)
Load an image file from the "res/img" directory. Compatible image types are jpg, png, and bmp. Magenta (255,0,255) is used as the transparent colour key.
> **file_name** _StringType_ - The name of the image file to load.

> **return** _Surface_ - The loaded image resource.

#####load_sound(file_name)
Load a sound file from the "res/snd" directory. Only ogg files are compatible.
> **file_name** _StringType_ - The name of the sound file to load.

> **return** _Sound_ - The loaded sound resource.

##ecs Module
TODO