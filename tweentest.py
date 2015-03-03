#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame import Rect
from pygame.sprite import Sprite, Group
from engine.game import Game, Scene
from engine.tween import Tweener, IN_OUT_QUAD
from engine.loader import load

class TestScene(Scene):
    name = "tweentest"
    
    def on_init(self):
        self.sprites = Group()
        self.smile_sprite = TestSprite()
        self.sprites.add(self.smile_sprite)
        self.tweener = Tweener()
    
    def on_cleanup(self):
        pass
    
    def on_update(self, delta, events):
        click = self.parent.mouse.click
        if click:
            x, y = click.x, click.y
            dx = x - self.smile_sprite.rect.centerx
            dy = y - self.smile_sprite.rect.centery
            self.tweener.remove_all_tweens()
            self.tweener.add_tween(self.smile_sprite, set_x=dx,
                    tween_type=IN_OUT_QUAD)
            self.tweener.add_tween(self.smile_sprite, set_y=dy,
                    tween_type=IN_OUT_QUAD)
        self.tweener.update(float(delta) / 1000.0)
    
    def on_render(self, screen):
        self.sprites.draw(screen)

class TestSprite(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = load("smile.bmp")
        self.rect = Rect(0, 0, 64, 64)
    
    def get_x(self):
        return self.rect.centerx
    
    def set_x(self, x):
        self.rect.centerx = x
    
    def get_y(self):
        return self.rect.centery
    
    def set_y(self, y):
        self.rect.centery = y

if __name__ == "__main__":
    game = Game(640, 480)
    pygame.display.set_caption("Tween Test")
    game.add_scene(TestScene)
    game.start()
