import pygame
from pygame.sprite import Sprite

class AnimatedSprite(Sprite):
    def __init__(self, spritemap, rect, *groups):
        Sprite.__init__(self, *groups)
        self.spritemap = spritemap
        self.rect = rect
        self.is_animating = False

        rows = spritemap.get_height() / rect.h
        columns = spritemap.get_width() / rect.w

        self.set_frame(0)


    def animate(self, frames, fps, loop=False, func=None):
        """
        sprite.animate([0,1,2,1], 5, True, some_func)
        """
        if not self.spritemap:
            raise "Cannot animate if spritemap is not set"
        self.is_animating = True
        self.elapsed_time = 0
        self.last_frame = 0
        self.frames = frames
        self.fps = fps
        self.loop = loop
        self.callback = func

    def update(self, delta):
        if not self.is_animating:
            return
        next_frame = self.last_frame
        num_frames = len(self.frames)
        self.elapsed_time = self.elapsed_time + delta
        elapsed_frames = int(self.elapsed_time / (1000 / self.fps))
        if elapsed_frames < num_frames:
            if not self.last_frame == elapsed_frames:
                next_frame = elapsed_frames
        elif elapsed_frames >= num_frames:
            if self.loop:
                next_frame = elapsed_frames % num_frames
            else:
                next_frame = num_frames - 1
                self.set_frame(self.frames[next_frame])
                self.is_animating = False
                func = self.callback
                if func:
                    func()
                return
        if not next_frame == self.last_frame:
            self.set_frame(self.frames[next_frame])
            self.last_frame = next_frame

    def set_frame(self, frame_index):
        map_width = self.spritemap.get_width()
        map_height = self.spritemap.get_height()
        frame_width = self.rect.w
        frame_height = self.rect.h
        columns = map_width / frame_width
        frame_row = frame_index / columns
        frame_column = frame_index % columns
        source_x = frame_column * frame_width
        source_y = frame_row * frame_height
        source_rect = pygame.Rect(source_x, source_y,
                                  frame_width, frame_height)
        self.image = self.spritemap.subsurface(source_rect)
