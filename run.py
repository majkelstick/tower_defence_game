import pygame

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    
    win = pygame.display.set_mode((1000, 700))
    from game import Game
    game = Game(win)
    game.run()
