import pygame
from functions import *
from  consts import *
from board import *

class Start_Screen:

    def __init__(self):
        self.display = screen
        self.weight = size[0]
        self.height = size[1]
        self.start_screen = load_image("logo.png")
        self.pos_start_screen = self.start_screen.get_rect(center=(self.weight // 2, self.height // 2 - 160))
        self.display.blit(self.start_screen, self.pos_start_screen)
        self.text_for_start_screen = load_image("text_for_start_screen.png")
        self.pos_text_for_start_screen = self.text_for_start_screen.get_rect(center=(self.weight // 2 + 10, self.height // 2 + 150))
        self.display.blit(self.text_for_start_screen, self.pos_text_for_start_screen )
        pygame.display.update()



class Vibor_igrokov:
    def __init__(self):
        self.display = screen
        self.num_of_players = [1, 2, 3, 4]
        self.FPS = FPS
        self.i = 1
        self.weight = size[0]
        self.height = size[1]
        font = pygame.font.Font(None, 200)
        text = font.render(f'{self.num_of_players[self.i % 2]}', True, pygame.Color("red"))
        place = text.get_rect(center=(self.weight // 2, self.height // 2 + 135))
        self.display.blit(text, place)
        self.run = True
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] or key[pygame.K_DOWN]:
                self.i += 1
                self.display.blit(text, place)
            elif key[pygame.K_SPACE]:
                    self.board = Board()
            pygame.display.flip()
            clock.tick(self.FPS)

        

