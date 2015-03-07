import os
import pygame

images = {}
sounds = {}

def load(file_name):
    file_ext = file_name.split(".")[-1]
    if (file_ext == "jpg" or file_ext == "png" or file_ext == "bmp"):
        return load_image(file_name)
    elif file_ext == "ogg":
        return load_sound(file_name)

def load_image(file_name):
    cached_image = images.get(file_name, None)
    if cached_image:
        return cached_image
    file_path = os.path.join("res/img/" + file_name)
    image = pygame.image.load(file_path)
    conv_image = image.convert()
    conv_image.set_colorkey(pygame.Color(255, 0, 255))
    #cache the image
    images[file_name] = conv_image
    return conv_image

def load_sound(file_name):
    cached_sound = sounds.get(file_name, None)
    if cached_sound:
        return cached_sound
    file_path = os.path.join("res/snd/" + file_name)
    sound = pygame.mixer.Sound(file_path)
    #cache the sound
    sounds[file_name] = sound
    return sound
