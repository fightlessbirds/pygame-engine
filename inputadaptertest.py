#!/usr/bin/env python

from pygame import Rect
from pygame.font import Font, get_default_font
from pygame.sprite import Sprite, Group
from engine.game import Game, Scene

class InputAdapterTest(Scene):
    name = "inputadaptertest"
    
    def on_init(self):
        self.sprites = Group()
        # keyboard
        self.keys_pressed = self.KeysPressed()
        self.sprites.add(self.keys_pressed)
        # mouse
        self.pos_sprite = self.MousePos()
        self.sprites.add(self.pos_sprite)
        self.clicks_sprite = self.MouseClicks()
        self.sprites.add(self.clicks_sprite)
        
    def on_update(self, delta, events):
        # keyboard
        self.keys_pressed.update(self.parent.keyboard)
        # mouse
        pos = self.parent.mouse.pos
        self.pos_sprite.update(pos)
        clicks = self.parent.mouse.clicks
        self.clicks_sprite.update(clicks)
        
    def on_render(self, screen):
        self.sprites.draw(screen)
        
    def on_cleanup(self):
        pass
        
    class KeysPressed(Sprite):
        def __init__(self):
            Sprite.__init__(self)
            self.rect = Rect(50, 150, 0, 0)
        
        def update(self, keyboard):
            self.image = default_font.render(str(keyboard), False,
                                             (255, 255, 255))

    class MousePos(Sprite):
        def __init__(self):
            Sprite.__init__(self)
            self.rect = Rect(50, 50, 0, 0)
            
        def update(self, pos):
            self.image = default_font.render(str(pos), False,
                                             (255, 255, 255))
    
    class MouseClicks(Sprite):
        def __init__(self):
            Sprite.__init__(self)
            self.rect = Rect(50, 100, 0, 0)
        
        def update(self, clicks):
            click_string = ""
            for click in clicks:
                click_string += "[x:{} y:{} button:{}] ".format(
                                         click.x, click.y, click.button)
            self.image = default_font.render(click_string, False,
                                             (255, 255, 255))

if __name__ == "__main__":
    game = Game(800, 600, title="InputAdapter Test", fullscreen=False,
                frame_rate=2)
    default_font = Font(get_default_font(), 18)
    game.add_scene(InputAdapterTest)
    game.start()
