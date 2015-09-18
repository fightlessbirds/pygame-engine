#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame import Rect
from pygame.sprite import Group

import engine
from engine.game import Game, Scene
from engine.loader import load
from engine.animation import AnimatedSprite

class TestScene1(Scene):
    name = "test"

    def on_init(self):
        self.test_sprites = Group()
        spritemap = load("animsprite.png")

        test_sprite = AnimatedSprite(self.test_sprites)
        test_sprite.spritemap = spritemap
        test_sprite.rect = Rect(100, 100, 16, 16)
        test_sprite.animate([0,1,2,1], 5, True)

    def on_cleanup(self):
        pass

    def on_update(self, delta, events):
        self.test_sprites.update(delta)

    def on_render(self, screen):
        self.test_sprites.draw(screen)

if __name__ == "__main__":
    game = Game(640, 480)
    pygame.display.set_caption("Animation Test")
    game.add_scene(TestScene)
    game.start()
