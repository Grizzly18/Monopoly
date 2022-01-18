import pygame
from win32api import GetSystemMetrics
from functions import *
from board import *

WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()
functs = {None: None, 0: terminate, 1: None, 2: None}
FPS = 120


class MainPage:
    def __init__(self):
        self.all_page_buttons = []
        self.all_page_buttons.append(Button(load_image("create.png", colorkey=-1), (WIDTH * 0.75, HEIGHT * 0.25)))
        text = font.render(f'Ожидают игры', True, pygame.Color("black"))
        place = text.get_rect(center=(WIDTH * 0.3, HEIGHT * 0.25))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    all_sprites.update(event) 
            pygame.display.flip()
            screen.fill(pygame.Color(247, 235, 235), pygame.Rect(WIDTH * 0.15, 0, WIDTH * 0.70, HEIGHT))
            screen.fill(pygame.Color(250, 242, 242), pygame.Rect(0, 0, WIDTH, HEIGHT / 100 * 15))
            screen.blit(text, place)
            all_sprites.draw(screen)
            all_sprites.update()
            clock.tick(FPS)

    def ex(self):
        for button in self.all_page_buttons:
            button.kill()
    

class MAIN:
    def __init__(self):
        Button(load_image("logo.png", colorkey=-1), (WIDTH / 100 * 16, HEIGHT / 100 * 7.5))
        Button(load_image("findgame.png", colorkey=-1), (WIDTH / 100 * 80, 65), 1)
        Button(load_image("login.png", colorkey=-1), (WIDTH / 100 * 93, 63), 2)
        Button(load_image("exit.png"), (WIDTH - 25, 15), 0)
        screen.fill(pygame.Color(214, 210, 210))
        MainPage()


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
    font = pygame.font.Font(None, 60)
    MAIN()
    pygame.quit()
