import pygame as py
from .enemy import Enemy
import os

py.display.init()

imgs = []
for x in range(20):
    add_str = str(x)
    if x < 10:
        add_str = "0" + add_str
    imgs.append(py.transform.scale(
        py.image.load(os.path.join("assets/enemies", "3_enemies_1_run_0" + add_str + ".png")).convert_alpha(),
        (64, 64)))

class Spellun(Enemy):

    def __init__(self):
        super().__init__()
        self.name = "spellun"
        self.money = 100
        self.max_of_life = 4
        self.life = self.max_of_life
        self.imgs = imgs
        self.velocity = 4
