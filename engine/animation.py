from pygame.sprite import Sprite

class AnimatedSprite(Sprite):
    def __init__(self, *groups):
        Sprite.__init__(self, *groups)
        self.is_animating = False

    def animate(self, frames, fps, loop=False, func=None):
        if not self.spritemap:
            raise "Cannot animate if spritemap is not set"
        self.is_animating = True
        self.elapsed_time = 0
        self.frames = frames
        self.num_frames = len(frames)
        self.fps = fps
        self.loop = loop
        self.callback = func

    def update(self, delta):
        if not self.is_animating:
            return
        self.elapsed_time = self.elapsed_time + delta
        elapsed_frames = int(self.elapsed_time / (1000 / self.fps))
        if elapsed_frames < self.num_frames:
            self.set_frame(elapsed_frames)
        elif elapsed_frames >= self.num_frames:
            if self.loop:
                next_frame = elapsed_frames % self.num_frames
                self.set_frame(next_frame)
            else:
                self.set_frame(self.num_frames - 1)
                self.is_animating = False
                func = self.callback
                if func:
                    func()

    def set_frame(self, frame_index):
        # use self.rect.w/h to split spritemap into frames and select the correct frame
        map_width = self.spritemap.width()
        map_height = self.spritemap.heigh()
        columns = int( self.rect.w)
