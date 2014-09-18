import os
import pygame


#TODO: Scenes will be organized by their name instead of a numeric index.
#TODO: When a scene is finished, it is destroyed. A new instance is created when the scene starts again.

class Game():
    """
    Attributes:
        frame_rate
        screen
        screen_rect
        background
        scenes
        current_scene
        next_scene
        finished
    """

    def __init__(self, width, height, fullscreen=False, frame_rate=30, title="PyGame Window", icon=None):
        """Initialize the game module. Creates a display window with the
        specified parameters."""
        print("Initializing game")
        #initialize pygame and the game screen
        pygame.init()
        self.frame_rate = frame_rate
        if (fullscreen == True):
            self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((width, height))
        #set the screen area rect
        self.screen_rect = pygame.Rect(0, 0, width, height)
        #set the window caption
        pygame.display.set_caption(title)
        #set the window icon
        if icon != None:
            pygame.display.set_icon(icon)
        #set the background colour
        self.background = 0, 0, 0
        #create the dictionary to store scenes.
        self.scenes = {}
        self.currentScene = None
        self.next_scene = None
        #attribute that controls when the game quits
        self.finished = False
        print("Game is ready for scenes")

    def add_scene(self, scene, name):
        """Add a scene to the game. If no scene has been added prior then
        this scene will be set as the default startup scene.
        scene - A subclass of Scene with all functions implemented.
        name - The name of the scene."""
        #add the scene to the dictionary of scene
        self.scenes[name] = scene
        #if no scenes have been added then make this the next scene
        if (self.next_scene == None):
            self.next_scene = name
        print("Scene " + name + " has been added to the game")
    
    def load_scene(self, name):
        """Returns an instance of the specified scene."""
        #get scene from scene dictionary
        scene_class = self.scenes[name]
        #create scene instance
        scene_object = scene_class(self)
        #the scene becomes a child of the game
        scene_object.parent = self
        return scene_object

    def set_next_scene(self, name):
        """Set the next scene.
        name - The name for the scene class which has been added to the game."""
        scene_class = self.scenes[name]
        if (scene_class == None):
            raise Exception("Could not find scene: " + name)
        self.next_scene = name
        print("Set next scene to " + name)

    def start(self):
        """Starts the game. Control is not passed back to the calling module
        until the game is finished. The game will not start if no scenes have
        been added. When the game ends PyGame will be shut down."""
        #will quit unless scenes are added
        if (len(self.scenes) == 0):
            raise Exception("cannot start game, there are no scenes")
        else:
            #the first scene to be added will be executed by default.
            while (self.finished == False):
                    self.current_scene = self.load_scene(self.next_scene)
                    print("Initializing scene: " + self.current_scene.get_name())
                    self.current_scene.on_init()
                    print("Beginning game loop")
                    clock = pygame.time.Clock() #create a new clock
                    while (self.current_scene.finished == False):   #main game loop
                        #check if the application should be closed
                        quit_event = pygame.event.get(pygame.QUIT)
                        if (quit_event):
                            print("Window manager exit request")
                            self.current_scene.finished = True
                            self.finished = True
                            break
                        events = pygame.event.get()
                        #control frame rate and get elapsed milliseconds
                        delta = clock.tick(self.frame_rate)
                        #update the scene
                        self.current_scene.on_update(delta, events)
                        #clear the screen buffer, render the scene,
                        #and flip the back buffer
                        pygame.draw.rect(self.screen, self.background, self.screen_rect)
                        self.current_scene.on_render(self.screen)
                        pygame.display.flip()
                    #do any necessary cleanup for the scene
                    print("Scene is finished. Cleaning up and switching to next scene")
                    self.current_scene.on_cleanup()
        #shut down pygame
        pygame.quit()

    def stop(self):
        """Stop the game."""
        self.current_scene.finished = True
        self.finished = True

    def get_width(self):
        return self.screen_rect.width

    def get_height(self):
        return self.screen_rect.height
    
    def load_image(self, file_name):
        file_path = os.path.join(file_name)
        image = pygame.image.load(file_path)
        conv_image = image.convert()
        return conv_image


class Scene:
    """A simple scene class with functions for init/cleanup and
    update/render loops. Simply override the functions, add an instance
    of the subclass to a game object, and start the game."""

    def __init__(self, game):
        self.parent = game
        self.finished = False

    def get_name(self):
        """Must be implemented to return the name by which this scene will be known."""
        raise NotImplementedError("Scene.get_name() is not implemented")

    def on_init(self):
        """Called before the game enters the update/render loop for
        this scene."""
        raise NotImplementedError("Scene.on_init() is not implemented")

    def on_update(self, delta, events):
        """Called once every iteration of the main loop. Game logic lives here.
        Arguments:
            game - The Game instance that this scene belongs to.
            delta - The amount of milliseconds that have passed since the
            last update."""
        raise NotImplementedError("Scene.on_update() is not implemented")

    def on_render(self, screen):
        """Called once every iteration of the main loop. Draw to the screen here.
        Arguments:
            game - The Game instance that this scene belongs to.
            screen - A pygame Surface instance that represents the screen."""
        raise NotImplementedError("Scene.on_render() is not implemented")

    def on_cleanup(self):
        """Cleanup any resources used by this scene. The scene instance is kept
        in memory, therefor any attributes that are not re-initialized in
        onInit() are retained the next time the scene is run.
        Arguments:
            game - The Game instance that this scene belongs to."""
        raise NotImplementedError("Scene.on_cleanup() is not implemented")
