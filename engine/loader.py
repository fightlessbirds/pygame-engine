"""
The loader module contains functions for loading resource files into
the game. Resources are cached so subsequent loading is almost
instantaneous.
"""


import os
import pygame


#global resource cache
images = {}


def load_image(file_name):
    """Load an image. Magenta is used as a color key."""
    cached_image = images.get(file_name, None)
    if cached_image:
        return cached_image
    
    file_path = os.path.join(file_name)
    image = pygame.image.load(file_path)
    conv_image = image.convert()
    conv_image.set_colorkey(pygame.Color(255, 0, 255))
    #cache the image
    images[file_name] = conv_image
    return conv_image
