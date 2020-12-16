import pygame as py
import os
from .tower import Tower

images = []
for x in (3, 6, 7):
    images.append(py.transform.scale(
        py.image.load("assets/towers/" + str(x) + ".png"), (60, 60)))

stone = py.transform.scale(py.image.load("assets/towers/40.png"), (22, 22))
ring = []
for x in (1,2):
    ring.append(py.transform.scale(py.image.load("assets/towers/" + str(x) + ".png"), (58, 14)))


class StoneTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.images = images
        self.range = 100
        self.width = images[self.level-1].get_width()
        self.height = images[self.level-1].get_height()
        self.price = [1000, 1500, 3000]
        self.name = "stone_tower"
        self.in_range = False
        self.life_damage = 1


    def draw(self, window):
        super().draw(window, stone, ring)