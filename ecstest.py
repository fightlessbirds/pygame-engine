import pygame
from pygame.locals import *
from engine.game import Game, Scene
from engine import ecs

class FooComponent(ecs.Component):
    name = "Foo"
    
    def on_init(self):
        def foofunc(variable):
            print("Foo func! {}".format(variable))
        self.parent.bind("FooEvent", foofunc)

class BarComponent(ecs.Component):
    name = "Bar"

class TestScene(Scene):
    name = "test"
    
    def on_init(self):
        def callback():
            print("Callback function")
        ecs.bind("Test", callback)
        ecs.install(FooComponent)
        ecs.install(BarComponent)
        e1 = ecs.Entity("Foo")
        ecs.Entity("Foo, Bar")
    
    def on_cleanup(self):
        ecs.destroy_all()
    
    def on_update(self, delta, events):
        if self.parent.keyboard.key_hit(K_SPACE):
            ecs.trigger("Test")
            ecs.trigger("FooEvent", 12345)
        elif self.parent.keyboard.key_hit(K_j):
            for e in ecs.query("Foo, Bar"): e.remove("Bar")
        elif self.parent.keyboard.key_hit(K_k):
            for e in ecs.query("Foo, Bar"): e.destroy()
        elif self.parent.keyboard.key_hit(K_l):
            ecs.Entity("Foo, Bar")
        print(ecs.query("Foo, Bar"))
    
    def on_render(self, screen):
        pass

game = Game(640, 480)
game.window_title = "Entity/Component System Test"
game.add_scene(TestScene)
game.start()
