from click import command
import pygame
from win32api import GetSystemMetrics
from functions import *
from board import *

WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()
functs = {None: None, 0: terminate, 1: None, 2: None}
FPS = 120


class Start_Screen:
    def __init__(self):
        self.display, running = screen, True
        Button(load_image("logo2.png", colorkey=-1), (130, 60))
        Button(load_image("findgame.png", colorkey=-1), (WIDTH / 100 * 80, 90), 1)
        Button(load_image("login.png", colorkey=-1), (WIDTH / 100 * 95, 88), 2)
        Button(load_image("exit.png"), (WIDTH - 25, 15), 0)
        # font = pygame.font.Font(None, 200)
        # text = font.render(f'', True, pygame.Color("red"))
        # place = text.get_rect(center=(self.weight // 2, self.height // 2 + 135))
        # screen.blit(text, place)
        self.display.fill(pygame.Color(214, 210, 210))
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    all_sprites.update(event) 
            pygame.display.flip()
            self.display.fill(pygame.Color(250, 242, 242), pygame.Rect(0, 0, WIDTH, HEIGHT / 100 * 15))
            all_sprites.draw(screen)
            all_sprites.update()
            clock.tick(FPS)

        pygame.display.update()


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos, command=None):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.command = command

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos):
                if functs[self.command] != None:
                    print(self.command)
                    functs[self.command]()

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Монополия")
    clock = pygame.time.Clock()
    Start_Screen()

    pygame.quit()
