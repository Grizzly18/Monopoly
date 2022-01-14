import pygame
from win32api import GetSystemMetrics
from functions import *
from board import *


width, height = 1600, 850
screen = pygame.display.set_mode((width, height))


class Start_Screen:
    def __init__(self):
        self.display = screen
        self.weight = width
        self.height = height
        self.start_screen = load_image("logo.png")
        self.pos_start_screen = self.start_screen.get_rect(center=(self.weight // 2, self.height // 2 - 160))
        self.display.blit(self.start_screen, self.pos_start_screen)
        self.text_for_start_screen = load_image("text_for_start_screen.png")
        self.pos_text_for_start_screen = self.text_for_start_screen.get_rect(center=(self.weight // 2 + 10, self.height // 2 + 150))
        self.display.blit(self.text_for_start_screen, self.pos_text_for_start_screen )
        pygame.display.update()



class Vibor_igrokov:
    def __init__(self):
        self.num_of_players = [1, 2, 3, 4]
        self.FPS = 60
        self.i = 1
        self.weight = width
        self.height = height
        font = pygame.font.Font(None, 200)
        text = font.render(f'{self.num_of_players[self.i % 4]}', True, pygame.Color("red"))
        place = text.get_rect(center=(self.weight // 2, self.height // 2 + 135))
        screen.blit(text, place)
        self.run = True
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                key = pygame.key.get_pressed()
                if key[pygame.K_UP]:
                    screen.fill(pygame.Color("black"), pygame.Rect(self.weight // 2 - 40, self.height // 2 + 60, self.weight // 2 - 680, self.height // 2 - 300))
                    self.i += 1
                    text = font.render(f'{self.num_of_players[self.i % 4]}', True, pygame.Color("red"))
                    place = text.get_rect(center=(self.weight // 2, self.height // 2 + 135))
                    screen.blit(text, place)
                elif key[pygame.K_DOWN]:
                    screen.fill(pygame.Color("black"), pygame.Rect(self.weight // 2 - 40, self.height // 2 + 60, self.weight // 2 - 680, self.height // 2 - 300))
                    self.i -= 1
                    text = font.render(f'{self.num_of_players[self.i % 4]}', True, pygame.Color("red"))
                    place = text.get_rect(center=(self.weight // 2, self.height // 2 + 135))
                    screen.blit(text, place)
                elif key[pygame.K_SPACE]:
                        self.board = Board()
            pygame.display.flip()
            pygame.display.update()
            clock.tick(self.FPS)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Монополия")
    clock = pygame.time.Clock()
    running = True
    sc = Start_Screen()
    begining = Vibor_igrokov()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
