import pygame as py
import time
import math

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.sell_price = [0, 0, 0]
        self.price = [0, 0, 0]
        self.level = 1
        self.selected = False
        self.menu = None
        self.images = []
        self.range = 0
        self.life_damage = 0
        self.animation_count = 0
        self.start_time = time.time()
        self.rising = True
        self.circle_color = (100, 190, 0, 50)


    def draw(self, window, object_img, ring):
        """
        draws the tower
        :param window: surface
        :return: None
        """
        if (self.in_range or self.animation_count > 0):

            if self.rising:
                self.animation_count += 4
                if self.animation_count > 40:
                    self.rising = False
            else:
                self.animation_count -= 4
                if self.animation_count < 0:
                    self.rising = True

        filling = py.Surface((self.range * 4, self.range * 4), py.SRCALPHA, 32)
        py.draw.circle(filling, self.circle_color, (self.range, self.range), self.range, 0)
        window.blit(filling, (self.x - self.range, self.y - self.range))
        image = self.images[self.level - 1]
        window.blit(ring[0], (self.x - 30, self.y - self.animation_count - 5))
        window.blit(image, (self.x - image.get_width() // 2, self.y - image.get_height() // 2))
        window.blit(ring[1], (self.x - 30, self.y - self.animation_count))
        if self.rising:
            window.blit(object_img, (self.x - 15, self.y - self.animation_count - 15))

    def clicked(self, x, y):
        """
        returns true if we clicked on a tower
        :param x: int
        :param y: int
        :return: bool
        """
        if x <= self.x + self.width and x >= self.x - self.width:
            if y <= self.y + self.height and y >= self.y - self.height:
                return True
        return False

    def upgrade(self):
        """
        upgrades the tower
        :return: None
        """
        self.level += 1
        self.range += 50

    def get_upgrade_cost(self):
        """
        returns upgrade cost
        :return:int
        """
        return self.price[self.level - 1]

    def attack(self, enemies):
        """
        attacks an enemy from an enemy list, then modifies the list
        :param enemies: list of enemies
        :return: None
        """
        money = 0
        to_kill = None
        max = 0
        if time.time() - self.start_time >= 1:
            self.start_time = time.time()
            for en in enemies:
                if math.sqrt((self.x - en.x) ** 2 + (self.y - en.y) ** 2) <= self.range:
                    if en.x > max:
                        max = en.x
                        to_kill = en
            if to_kill:
                self.in_range = True
                if to_kill.hit(self.life_damage):
                    enemies.remove(to_kill)
                    money = to_kill.money
            else:
                self.in_range = False
        return money

    def move(self, x, y):
        """
        moves a tower when we click on it
        :param x: int
        :param y: int
        :return: None
        """
        self.x = x
        self.y = y
