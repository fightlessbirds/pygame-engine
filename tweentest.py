#!/usr/bin/env python

import pygame
from pygame.locals import *
import engine
from engine.game import Game
from engine.game import Scene
from engine.tween import Tweener
from engine.loader import load

class TestScene(Scene):
    name = "tweentest"
    
    def on_init(self):
        self.sprites = Group()
        self.smile_sprite = Sprite()
        self.smile_sprite.image = load("smile.bmp")
        self.tweener = Tweener()
        tween self.tweener.addTween()
    
    def on_cleanup(self):
        pass
    
    def on_update(self, delta, events):
        
    
    def on_render(self, screen):
        

if __name__ == "__main__":
    game = Game(640, 480)
    pygame.display.set_caption("Tween Test")
    game.add_scene(TestScene)
    game.start()
