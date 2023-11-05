import pygame

class AnimationSprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(groups)

        self.elapsed_time = 0
        self.active_anim = None
        self.active_name = ""
        self.animation_storage = {}

    def move(self, dt):
        self.elapsed_time+=dt

    def store_animation(self, name, anim):
        self.animation_storage[name]=anim

        if self.active_name == "":
            self.set_active_animation(name)

    def set_active_animation(self, name):
        if name not in self.animation_storage.keys():
            print("no anim name")
            Return
        if name == self.active_name:
            return

        self.active_name = name
        self.active_anim = self.animation_storage[name]
        self.elapsed_time = 0

    def is_animation_finish(self):
        return self.active_anim.is_animation_finish(self.elapsed_time)