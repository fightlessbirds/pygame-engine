import pygame
from pygame.sprite import Group, Sprite
from pygame.font import Font
from pygame.locals import *

class ButtonGroup(Group):
    def update(self, mouse):
        if mouse.button_hit(1):
            Group.update(self, mouse.x, mouse.y)

class Button(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.rect = Rect(0, 0, 0, 0)
    
    def update(self, mouse_x, mouse_y):
        if self.is_clicked(mouse_x, mouse_y):
            self.on_click()
    
    def is_clicked(self, mouse_x, mouse_y):
        """Returns True/False if the button had been clicked"""
        if (mouse_x >= self.rect.left
                and mouse_x <= self.rect.right
                and mouse_y >= self.rect.top
                and mouse_y <= self.rect.bottom):
            return True
        return False
    
    def on_click(self):
        """Called when the button had been clicked on."""
        pass


class TextButton(Button):
    def __init__(self, text, font_size, color=Color("white")):
        Button.__init__(self)
        self.font = Font(None, font_size)
        self.font_color = color
        self.image = self.font.render(text, True, self.font_color)
        self.rect = Rect(0, 0, self.image.get_width(), self.image.get_height())


class ImageButton(Button):
    def __init__(self, image):
        Button.__init__(self)
        self.image = image
        self.rect = Rect(0, 0, image.get_width(), image.get_height())
