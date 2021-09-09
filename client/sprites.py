import random

import pygame
from pygame.locals import *


class Score:
    def __init__(self):
        self.game_score = 0


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super(Sprite, self).__init__()

    @staticmethod
    def load_image(image, size):
        curr_image = pygame.image.load(image)
        curr_image.set_colorkey((0, 0, 0), RLEACCEL)
        curr_image = pygame.transform.scale(curr_image, size)
        return curr_image


class Player(Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.fast = 0
        self.images_running = []

        self.image_run_count = 0
        while self.image_run_count < 10:
            self.image_run_str = "assets/Player/Run__00" + str(self.image_run_count) + ".png"
            self.images_running.append(Sprite.load_image(image=self.image_run_str, size=(150,150)))
            self.image_run_count = self.image_run_count + 1

        self.index_running = 0
        self.image_running = self.images_running[self.index_running]

        self.curr_image = self.image_running
        self.rect = pygame.Rect(50, 500, 100, 100)

    def update(self, pressed_keys):
        if pressed_keys[K_SPACE]:
            self.fast += 1
            if self.fast > 4:
                self.index_running = self.index_running + 1
                if self.index_running >= len(self.images_running):
                    self.index_running = 0
                self.image_running = self.images_running[self.index_running]
                self.curr_image = self.image_running
                self.fast = 0
        else:
            self.curr_image = self.images_running[0]

        if self.rect.right < 0:
            self.kill()


class Apple(Sprite):
    def __init__(self):
        super(Apple, self).__init__()
        self.image_apple_path = "assets/apple.png"
        self.curr_image = Sprite.load_image(image=self.image_apple_path, size=(50, 50))
        self.rect = pygame.Rect(1200, 600, 100, 100)

    def update(self, pressed_keys, apples, sprites):
        if pressed_keys[K_SPACE]:
            self.rect.move_ip(-2.5, 0)

        if self.rect.right < 0:
            self.kill()
