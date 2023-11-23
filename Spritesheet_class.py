import pygame

class Spritesheet:
    def __init__(self, filename, bg=None):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        self.bg = bg
        
    def get_image(self, frame, scale = None, flip = False):
        image = self.sprite_sheet.subsurface(pygame.Rect(frame))

        if scale is not None:
            width = frame[2]
            height = frame[3]
            image = pygame.transform.scale(image, (width*scale, height*scale))
        if flip:
            image = pygame.transform.flip(image, True, False)

        if self.bg is not None:
            image.set_colorkey(self.bg)
        return image

    def get_animation(self, coords, scale = None, flip = None):
        frames = [self.get_image(frame, scale, flip) for frame in coords]
        # return Animation(frames, frame_duration)
        return frames