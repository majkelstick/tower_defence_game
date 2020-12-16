import pygame as py
import os
from enemies.horse import Horse
from enemies.enemy import Enemy
from enemies.ghost import Ghost
from enemies.spellun import Spellun
from towers.stoneTower import StoneTower
from towers.fireTower import FireTower
from menu import PauseButton
from menu import Menu
from menu import BuyButton
from utilities import load_image
import time
import random



life_image = load_image("assets/heart.png", 30, 30)
money_image = load_image("assets/money.png", 30, 30)
play_button = load_image("assets/ui/menu/Play2.png", 40, 40)
pause_button = load_image("assets/ui/menu/Pause2.png", 40, 40)
sound_button = load_image("assets/ui/menu/Sound2.png", 80, 50)
nosound_button = load_image("assets/ui/menu/NoSound2.png", 50, 50)
frame =  load_image("assets/ui/frame.png", 170, 80)
upgrade_frame = py.transform.scale(frame, (90, 135))
menu_frame = py.transform.scale(frame, (200, 135))
game_over_frame = py.transform.scale(frame, (400, 300))
game_over = load_image("assets/ui/game_over.png", 200, 50)

stone_tower_images = []
for x in (3, 6, 7):
    stone_tower_images.append(load_image("assets/towers/"+ str(x) + ".png", 50, 50))

fire_tower_images = []
for x in (12, 14, 13):
    fire_tower_images.append(load_image("assets/towers/" + str(x) + ".png", 50, 50))


class Game:
    def __init__(self, win):
        py.mixer.music.load(os.path.join("assets", "music.mp3"))
        self.width = 1000
        self.height = 700
        self.window = win
        self.enemies = []
        self.towers = []
        self.lives = 10
        self.points = 0
        self.money = 1200
        self.paused = False
        self.music_on= True
        self.background = py.image.load(os.path.join("assets","tile1.png"))
        self.background = py.transform.scale(self.background, (self.width, self.height))
        self.clicks = []
        self.start_time = time.time()
        self.life_font = py.font.SysFont("georgia", 40, 1)
        self.points_font = py.font.SysFont("georgia", 40, 1)
        self.pauseButton = PauseButton(play_button, pause_button, self.width-150, self.height-65)
        self.soundButton = PauseButton(nosound_button, sound_button, self.width-100, self.height-70)
        self.menu = Menu(0, 0, menu_frame)
        self.menu.add_btn(1000, stone_tower_images[0], "STONE TOWER")
        self.menu.add_btn(3000, fire_tower_images[0], "FIRE TOWER")
        self.moving_tower = None
        self.upgrade_menu = None

#gdzie przeskalowac obraz wiezy??

    def run(self):
        py.mixer.music.play(loops=-1)
        run = True
        clock = py.time.Clock()
        while run:
            position = py.mouse.get_pos()

            #if self.moving_tower:
             #   self.moving_tower(pos[0], pos[1])
            pos = py.mouse.get_pos()

            # check for moving object
            if self.moving_tower:
                self.moving_tower.move(pos[0], pos[1])

            if self.paused:
                py.mixer.music.pause()
                for event in py.event.get():
                    if event.type == py.QUIT:
                        run = False
                    if event.type == py.MOUSEBUTTONDOWN:
                        if self.pauseButton.click(position[0], position[1]):
                            self.paused = not(self.paused)
                            self.pauseButton.paused = self.paused
                time.sleep(0.1)

            else:
                if self.music_on:
                    py.mixer.music.unpause()
                if time.time()-self.start_time >= 2:
                    self.start_time = time.time()
                    self.enemies.append(random.choice([Spellun(),Horse(), Ghost()]))
                clock.tick(200)

                for event in py.event.get():
                    if event.type == py.QUIT:
                        run = False
                    position = py.mouse.get_pos()

                    if event.type == py.MOUSEBUTTONDOWN:

                        if self.pauseButton.click(position[0], position[1]):
                                self.paused = not (self.paused)
                                self.pauseButton.paused = self.paused

                        if self.soundButton.click(position[0], position[1]):
                            self.music_on = not(self.music_on)
                            self.soundButton.paused = self.music_on
                            if self.music_on:
                                py.mixer.music.unpause()
                            else:
                                py.mixer.music.pause()

                        # look if you click on tower menu
                        tower_button = self.menu.get_clicked(position[0], position[1])
                        if tower_button:
                            cost = self.menu.buttons[tower_button-1].get_cost()
                            print(cost)
                            if self.money >= cost:
                                self.money -= cost
                            self.add_tower(tower_button-1)

                        #checks if you clicked on a tower
                        for tower in self.towers:
                            if tower.clicked(position[0], position[1]):
                                print("tower clicked!")
                                if (self.upgrade_menu):
                                    self.upgrade_menu = None
                                    self.tower_to_upgrade = None
                                else:
                                    if tower.level<3:
                                        self.tower_to_upgrade = tower
                                        self.upgrade_menu = Menu (tower.x - upgrade_frame.get_width()/2, tower.y - upgrade_frame.get_height()*1.5, upgrade_frame)
                                        if tower.name == "stone_tower":
                                            self.upgrade_menu.add_btn(tower.price[tower.level], stone_tower_images[tower.level], "UPGRADE")
                                        else:
                                            self.upgrade_menu.add_btn(tower.price[tower.level], fire_tower_images[tower.level], "UPGRADE")

                        #chcecks if you clicked on upgrade menu
                        if self.upgrade_menu:
                            if self.upgrade_menu.get_clicked(position[0], position[1]):
                                cost = self.tower_to_upgrade.get_upgrade_cost()
                                if self.money >= cost:
                                    self.money -= cost
                                    self.tower_to_upgrade.upgrade()


                    if event.type == py.MOUSEBUTTONUP:
                        if self.moving_tower:
                            self.towers.append(self.moving_tower)
                            self.moving_tower = None
                        #self.clicks.append(position)
                        #print(self.clicks)

                for en in self.enemies:
                    if en.x > self.width - 20 or en.y < 0 or en.y > self.height - 20 :
                        self.enemies.remove(en)
                        self.lives-=1

                for t in self.towers:
                    points = t.attack(self.enemies)
                    self.points += points
                    self.money += points

                self.draw()
       
    def draw (self):
        self.window.blit(self.background, (0, 0))
        #for c in self.clicks: #rysuje  czerwona kropke przy kliknieciu
         #   py.draw.circle(self.win, (255, 0, 0),(c[0], c[1]), 5, 0)
        for en in self.enemies:
            en.draw(self.window)
        for t in self.towers:
            t.draw(self.window)

        #draw upgrade menu
        if self.upgrade_menu:
            self.upgrade_menu.draw(self.window)

        #draw moving tower
        if self.moving_tower:
            self.moving_tower.draw(self.window)

        #draw lives
        life_num = self.life_font.render(str(self.lives), 1, (0, 0, 0))
        start_x = self.width
        self.window.blit(life_num, (start_x - life_image.get_width() * self.lives - 60, 0))
        for l in range(self.lives):
            self.window.blit(life_image, (start_x - life_image.get_width() * l - 30, 10))

        #draw money
        money_num = self.life_font.render(str(self.money), 1, (0, 0, 0))
        start_x = self.width
        self.window.blit(money_num, (start_x - len(str(self.money)) * 15 - 75, 40))
        self.window.blit(money_image, (start_x - money_image.get_width(), 50))

        #draw points
        points_num = self.points_font.render("Points:  " + str(self.points), 1, (250, 200, 0))
        self.window.blit(points_num, (self.width - 300, self.height - 150))


        if self.lives < 1:
            self.window.blit(game_over_frame, ((self.width - game_over_frame.get_width()) / 2, ((self.height - game_over_frame.get_height()) / 2)))
            self.window.blit(game_over, ((self.width - game_over_frame.get_width()) / 2 + 90, (self.height - game_over_frame.get_height()) / 2 + 15))
            self.paused = True

        self.menu.draw(self.window)
        # draw pause button
        self.window.blit(frame, (self.width - 175, self.height - 85))
        self.pauseButton.draw(self.window)
        self.soundButton.draw(self.window)
        #self.menu.draw(self.win)


        py.display.update()

    def draw_menu(self):
        pass

    def add_tower(self, index):
        x, y = py.mouse.get_pos()
        tower_list = [StoneTower(x, y), FireTower(x, y)]
        tower = tower_list[index]
        self.moving_tower = tower
        tower.moving = True


