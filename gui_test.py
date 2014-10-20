import pygame
from pygame import Color
from engine.game import Game, Scene
from engine.gui import ButtonGroup, TextButton, ImageButton


class GuiTestScene(Scene):
	name = "guitest"
	
	def on_init(self):
		self.buttons = ButtonGroup()
		
		text_button = TextButton("test", 200, Color("green"))
		def func_1():
			print("clicked text button")
		text_button.on_click = func_1
		text_button.rect.center = (200, 200)
		self.buttons.add(text_button)
		
		image = self.parent.load_image("test_resources/smile.bmp")
		image_button = ImageButton(image)
		def func_2():
			print("clicked image button")
		image_button.on_click = func_2
		image_button.rect.center = (250, 400)
		self.buttons.add(image_button)
	
	def on_update(self, delta, events):
		self.buttons.update()
	
	def on_render(self, screen):
		self.buttons.draw(screen)
	
	def on_cleanup(self):
		pass


if __name__ == "__main__":
	game = Game(800, 600)
	pygame.display.set_caption("GUI Test")
	game.add_scene(GuiTestScene)
	game.start()
