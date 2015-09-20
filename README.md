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
The game class is at the heart of the engine. It contains the core game update loop. Scene classes are aggregated by a Game object and instantiated on-the-fly. Game composes KeyboardAdapter and MouseAdapter objects.
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
> **width** _int_ - Width of the screen in pixels.

> **height** _int_ - Height of the screen in pixels.

> **fullscreen** _bool_ - Whether the game should be in fullscreen mode.

> **frame_rate** _int_ - The maximum frame rate that the game will run at.

> **title** _str_ - The title of the game displayed by the window manager.

#####add_scene(scene)
Add a Scene subclass to the Game object.
> **scene** _Scene_ - A subclass of Scene. Note that it will not work with an instance of a Scene subclass. It must be the subclass itself. Game will instantiate the subclass when the scene is loaded.

#####set_next_scene(name)
Set the scene that is to be loaded after the current scene is finished. Raises an exception if the scene cannot be found.
> **name** _str_ - The name of the Scene to be loaded. Must be the same as Scene.name.

#####start()
Start the game engine. At least one Scene subclass must be added or an exception is raised. If the next scene has not been explicitly set then the first scene that was added is loaded by default.
#####stop()
Stop the game engine. Sets the current Scene object as finished. Sets the Game object as finished.
#####get_width()
> **return** _int_ - The width of the game window.

#####get_height()
> **return** _int_ - The height of the game window.

###Scene Class
The Scene class encapsulates a scene in the game. Every scene has four functions that are called by its parent Game object and must be implemented: on\_init, on\_update, on\_render, and on_cleanup.
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
> **delta** _int_ - Elapsed milliseconds since the last update.

> **events** _[EventType]_ - A list of PyGame user events that occured since the last update.

#####on_render(screen)
Called when it is time to draw the scene to the screen.
> **screen** _Surface_ - The Surface object for the game screen.

#####on_cleanup()
Called after the scene has finished but before it is unloaded.
##animation Module
###AnimatedSprite Class
A Pygame sprite that can be animated. The rect and image attributes from the Sprite class are used in combination with a sprite map and the animate() function.
####Attributes
#####spritemap
A Pygame Surface object that contains the frames the sprite should draw from. All frames must be the same size as the sprite's rect attribute.
#####is_animating
A boolean that controls whether the sprite should be animating. This is automatically set to True by the animate() function. Can be used to interrupt an animation in progress.
####Functions
#####\_\_init\_\_(spritemap, rect, *groups)
AnimatedSprite constructor. Creates a new animated sprite from a spritemap and rect. The first frame is set as the sprite image automatically.
> **spritemap** _Surface_ - A Pygame Surface object containing the frames for the sprite.

> **rect** _Rect_ - Pygame rect object that stores the frame size.

> **groups** _Group_ - One or more Pygame sprite groups that the sprite should be added to.

#####animate(frames, fps, loop=False, func=None)
Start animating the sprite. The spritemap and rect atttributes must already be set.
> **frames** _[int]_ - An array of integers that represent the frames of the animation. Index starts at 0.

> **fps** _int_ - The speed at which to animate in frames per second.

> **loop** _bool_ - Whether or not to loop the animation. If looped the callback function will never be called.

> **func** _function_ - A function to call when the animation finishes. This will only be called if loop is set to false. Setting the is_animate attribute to False will not trigger this callback.

#####set_frame(frame_index)
Set the current image to a frame from the spritemap. Spritemap and rect attributes must be set.
> **frame_index** _int_ - The index for the frame to set. Index starts at 0.

##event Module
####Functions
#####bind(event, callback)
Bind a callback function to an event.
> **event** _str_ - The event to bind.

> **callback** _function_ - The function to be called when the event is triggered. It may or may not have a *args argument.

#####unbind(event, callback)
Unbind a callback from an event.
> **event** _str_ - The event to unbind.

> **callback** _function_ - The callback function to unbind.

#####trigger(event, *args)
Trigger an event globally.
> **event** _str_ - The event to trigger.

> **args** - Arguments to pass along to the callback function.

###TimedEventSystem Class
This class manages one-shot timed events. Events can be created with a delay and a callback function for when they are finished.
####Functions
#####add(delay, func)
Add a new TimedEvent to the system.
> **delay** _int_ - The amount of milliseconds that must pass until the timer runs out.

> **func** _function_ - The callback function that will be called when the timer runs out.

> **return** _TimedEvent_ - The newly created event object.

#####remove(event)
Remove an event from the system before it has a chance to trigger.
> **event** _TimedEvent_ - The event object ot be removed.

#####update(delta)
Update all TimedEvent objects belonging to this system.
> **delta** _int_ - The amount of milliseconds that have elapsed since the last update.

##gui Module
The gui module contains some classes for creating GUI elements that the player can click on.
###ButtonGroup Class
A sprite group that manages and updates Button objects. Inherits from the PyGame Group class.
####Functions
#####update(mouse)
Update the button group, checking if any of the buttons have been clicked.
> **mouse** _MouseAdapter_ - The MouseAdapter object to check for clicks.

###Button Class
Base class for buttons. Instances are aggregated by the ButtonGroup class.
####Functions
#####update(mouse\_x, mouse_y)
Inherited from the PyGame Sprite class. Called by the parent ButtonGroup.
> **mouse_x** _int_ - Mouse position on the x-axis.

> **mouse_y** _int_ - Mouse position on the y-axis.

#####on_click()
Called when the button is clicked. Override this to create a callback function for the button.

###TextButton Class
A button that appears as text.
####Functions
#####\_\_init\_\_(text, font_size, color=(255, 255, 255))
TextButton class constructor.
> **text** _str_ - The text to be displayed on the button.

> **font_size** _int_ - The font size used to render the text.

> **color** _(int)_ - A tuple of three integers ranging 0-255. The colour for the text.

###ImageButton Class
A button that appears as an image.
####Functions
#####\_\_init\_\_(image)
ImageButton class constructor. Create a new button that appears as an image.
> **image** _Surface_ - The image to be displayed on the button. A PyGame Surface object.

##inputadapter Module
This module contains classes that make it easy to get input from the player. The input adapter classes are composed by the Game class.
###KeyboardAdapter Class
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
> **key_code** _int_ - The PyGame key code for the key to check.

> **return** _bool_ - True/False if the key is being held down.

#####key\_hit(key_code)
Check if a key has just been pressed since the last update.
> **key_code** _int_ - The PyGame key code for the key to check.

> **return** _bool_ - True/False if the key was pressed.

###Keystroke Class
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
> **value** _int_ - PyGame key code for which key this Keystroke object should represent.

####\_\_str\_\_()
String representation of the KeyboardAdapter object.
> **return** _str_ - Returns a string built from the keys that were pressed since the last update.

###MouseAdapter Class
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
###Click Class
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
> **pos** _(int)_ - A tuple containing the x and y location where the mouse was clicked.

> **button** _int_ - PyGame button code for the button that was pressed.

##loader Module
The loader module contains functions for loading game resources. Resources are cached to save memory and time for when they are loaded again later.
####Functions
#####load(file_name)
Load a resource. The type of resource is determined automatically by the file extention.
> **return** _Surface/Sound_ - The loaded resource.

#####load\_image(file_name)
Load an image file from the "res/img" directory. Compatible image types are jpg, png, and bmp. Magenta (255,0,255) is used as the transparent colour key.
> **file_name** _str_ - The name of the image file to load.

> **return** _Surface_ - The loaded image resource.

#####load\_sound(file_name)
Load a sound file from the "res/snd" directory. Only ogg files are compatible.
> **file_name** _str_ - The name of the sound file to load.

> **return** _Sound_ - The loaded sound resource.

##tween Module
TODO