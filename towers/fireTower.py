import pygame as py
import os
from .tower import Tower

images = []
for x in (12, 14, 13):
    images.append(py.transform.scale(py.image.load("assets/towers/" + str(x) + ".png"), (60, 60)))
ring = []
for x in (8, 9):
    ring.append(py.transform.scale(py.image.load("assets/towers/" + str(x) + ".png"), (58, 14)))

fire = py.transform.scale(py.image.load("assets/towers/35.png"), (22, 22))


class FireTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.images = images
        self.range = 150
        self.width = images[self.level - 1].get_width()
        self.height = images[self.level - 1].get_height()
        self.price = [3000, 3000, 9000]
        self.name = "fire_tower"
        self.in_range = False
        self.life_damage = 2

    def draw(self, window):
        super().draw(window, fire, ring)

