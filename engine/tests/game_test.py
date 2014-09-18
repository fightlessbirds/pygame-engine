from engine.game import *


class TestScene1(Scene):
    def on_init(self):
        print("Now initializing test1")
        self.test_image = draw_test_image(1)
        self.smile_image = self.parent.load_image("engine/tests/smile.png")
    
    def get_name(self):
        return "test1"
    
    def on_cleanup(self):
        pass
    
    def on_update(self, delta, events):
        for event in events:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_2):
                self.parent.set_next_scene("test2")
                self.finished = True
    
    def on_render(self, screen):
        test_image_w = self.test_image.get_width()
        test_image_h = self.test_image.get_height()
        screen.blit(self.test_image, pygame.Rect(0, 0, test_image_w, test_image_h))
        smile_w = self.smile_image.get_width()
        smile_h = self.smile_image.get_height()
        screen.blit(self.smile_image, pygame.Rect(0, 128, smile_w, smile_h))


class TestScene2(Scene):
    def on_init(self):
        print("Now initializing test2")
        self.test_image = draw_test_image(2)
        self.smile_image = self.parent.load_image("engine/tests/smile.png")
    
    def get_name(self):
        return "test2"
    
    def on_cleanup(self):
        pass
    
    def on_update(self, delta, events):
        for event in events:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_1):
                self.parent.set_next_scene("test1")
                self.finished = True
    
    def on_render(self, screen):
        test_image_w = self.test_image.get_width()
        test_image_h = self.test_image.get_height()
        screen.blit(self.test_image, pygame.Rect(0, 0, test_image_w, test_image_h))
        smile_w = self.smile_image.get_width()
        smile_h = self.smile_image.get_height()
        screen.blit(self.smile_image, pygame.Rect(0, 128, smile_w, smile_h))

def draw_test_image(number):
    """Return a Surface object with some text combined with a number."""
    font = pygame.font.Font(pygame.font.get_default_font(), 18)
    image = font.render("Current scene is " + str(number) + ". Press 1 or 2 on the keyboard to switch scenes",
                        False, pygame.Color("white"))
    return image

def run():
    game = Game(640, 480)
    pygame.display.set_caption("Game Test")
    game.add_scene(TestScene1, "test1")
    game.add_scene(TestScene2, "test2")
    game.start()
