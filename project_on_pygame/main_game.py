import pygame
from win32api import GetSystemMetrics
from functions import *
from board import *


WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 120


class Start_Screen:
    def __init__(self):
        self.display = screen
        self.start_screen = load_image("logo2.png", colorkey=-1)
        self.pos_start_screen = self.start_screen.get_rect(center=(130, 60))
        self.game = load_image("findgame.png", colorkey=-1)
        self.pos_game = self.start_screen.get_rect(center=(WIDTH / 100 * 80, 90))
        self.login = load_image("login.png", colorkey=-1)
        self.pos_login = self.start_screen.get_rect(center=(WIDTH / 100 * 95, 88))
        self.exit = load_image("exit.png")
        self.pos_exit = self.start_screen.get_rect(center=(WIDTH + 65, 55))
        running = True
        # font = pygame.font.Font(None, 200)
        # text = font.render(f'', True, pygame.Color("red"))
        # place = text.get_rect(center=(self.weight // 2, self.height // 2 + 135))
        # screen.blit(text, place)
        self.display.fill(pygame.Color(214, 210, 210))
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
            self.display.fill(pygame.Color(250, 242, 242), pygame.Rect(0, 0, WIDTH, HEIGHT / 100 * 15)), self.display.blit(self.start_screen, self.pos_start_screen), self.display.blit(self.game, self.pos_game), self.display.blit(self.login, self.pos_login), self.display.blit(self.exit, self.pos_exit)
            clock.tick(FPS)

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
    Start_Screen()

    pygame.quit()
