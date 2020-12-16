import pygame as py
import os
py.font.init()

star = py.image.load(os.path.join("assets", "star.png"))
money_image = py.transform.scale(py.image.load(os.path.join("assets", "money.png")), (10, 10))

class Menu: #item_menu? tower_menu?
    def __init__(self, x, y, background):
        self.x = x #lewy gorny rog!
        self.y = y
        self.width = background.get_width()
        self.height = background.get_height()
        self.buttons = []
        self.bg = background
        self.font = py.font.SysFont("cambria", 18)
        self.name_font = py.font.SysFont("cambria", 12)


    def add_btn(self, cost, button_img, name):
        """
        adds buttons to menu
        :param img: surface
        :param name: str
        :return: None
        """
        self.buttons.append(BuyButton(self, cost, len(self.buttons), button_img, name))

    def draw(self, window):
        """
        draws buttons and menu background
        :param window: surface
        :return: None
        """
        window.blit(self.bg, (self.x, self.y))
        for btn in self.buttons:
            btn.draw(window)
            text = self.font.render(str(btn.get_cost()), 1, (255, 255, 255))
            window.blit(money_image, (btn.x + text.get_width(), btn.y + 61))
            window.blit(text, (btn.x + btn.width - 55, btn.y + 55))
            name = self.name_font.render(btn.name, 1, (250, 200, 0))
            window.blit(name, (btn.x - 10, btn.y - 20))


    def get_clicked(self, X, Y):
        """
        return the clicked item from the menu
        :param X: int
        :param Y: int
        :return: int
        """
        for btn in self.buttons:
            if btn.click(X,Y):
                return btn.btn_count+1

        return None

    def update(self):
        """
        update menu and button location
        :return: None
        """
        for btn in self.buttons:
            btn.update()

class Button:
    """
    general class for buttons
    """
    def __init__(self, menu, img, name):
        self.name = name
        self.img = img
        self.menu = menu
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = menu.x
        self.y = menu.y

    def click(self, x, y):
        """
        returns true if the clicked position was within the button
        :param x: int
        :param y: int
        :return: bool
        """
        if self.x <= x <= self.x+self.width:
            if self.y <= y <= self.y + self.height:
                return True
        return False

    def draw(self, win):
        """
        draws the button
        :param win: surface
        :return: None
        """
        #for img in self.img:
        win.blit(self.img, (self.x, self.y))

    #def update(self):
        #self.x = self.menu.x - 50
        #self.y = self.menu.y - 110




class BuyButton(Button):

    def __init__(self, menu, cost, btn_count, img, name):
        self.name = name
        self.cost = cost
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = menu.x + btn_count*100 + 20
        self.y = menu.y + menu.height/4
        self.btn_count = btn_count

    def get_cost(self):
        """
        gets cost of upgrade to next level
        :return: int
        """
        return self.cost



class PauseButton(Button):
    def __init__(self, play_img, pause_img, x, y):
        self.img = play_img
        self.play = play_img
        self.pause = pause_img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.paused = False

    def draw(self, win):
        if self.paused:
            win.blit(self.play, (self.x, self.y))
        else:
            win.blit(self.pause, (self.x, self.y))

