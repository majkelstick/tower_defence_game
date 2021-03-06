import pygame as py
from .enemy import Enemy
import os



imgs = []
for x in range(20):
    add_str = str(x)
    if x < 10:
        add_str = "0" + add_str
    imgs.append(py.transform.scale(
        py.image.load(os.path.join("assets/enemies", "9_enemies_1_run_0" + add_str + ".png")).convert_alpha(),
        (64, 64)))

class Ghost(Enemy):

    def __init__(self):
        super().__init__()
        self.name = "ghost"
        self.money = 100
        self.max_of_life = 1
        self.life = self.max_of_life
        self.imgs = imgs
        self.velocity = 10
