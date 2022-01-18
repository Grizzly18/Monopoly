from glob import glob
from socket import socket
import pygame
from win32api import GetSystemMetrics
from functions import *
from Socket import Socket
import asyncio
from threading import Thread

WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()
functs = {None: None, 0: terminate, 1: "MainPage", 2: "Login"}
FPS = 120
messages, online, NowPage = "", False, "MainPage"

def translate(word):
    if (len(word) <= 0):
        return ""
    new_word = {}
    for i in word.split("!!!"):
        t = i.split('#')
        if (t == ['']):
            continue
        new_word[t[0]] = t[1].split(',')
    return new_word

def Game(y):
    screen.fill(pygame.Color(247, 235, 235), pygame.Rect(WIDTH * 0.15, y, WIDTH * 0.70, y + 60))

class MainPage:
    def __init__(self):
        global messages, client, NowPage
        if online:
            client.send_data("check listgame")

        self.all_page_buttons = []
        self.all_page_buttons.append(Button(load_image("create.png", colorkey=-1), (WIDTH * 0.75, HEIGHT * 0.25)))
        self.all_games = translate(messages)
        text = font.render(f'Ожидают игры', True, pygame.Color("black"))
        place = text.get_rect(center=(WIDTH * 0.3, HEIGHT * 0.25))
        screen.fill(pygame.Color(250, 242, 242), pygame.Rect(0, 0, WIDTH, HEIGHT / 100 * 15))
        screen.fill(pygame.Color(247, 235, 235), pygame.Rect(WIDTH * 0.15, HEIGHT * 0.15, WIDTH * 0.70, HEIGHT))
        for i in range(1, len(self.all_games) + 1):
            Game(HEIGHT * 0.15 + (i * 80))
        while NowPage == "MainPage":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    all_sprites.update(event) 
            pygame.display.flip()
            screen.blit(text, place)
            all_sprites.draw(screen)
            all_sprites.update()
            clock.tick(FPS)


class Login:
    def __init__(self):
        self.login = ''
        self.password = ''
        self.font = pygame.font.Font(None, 32)
        self.font1 = pygame.font.Font(None, 48)
        self.login_rect = pygame.Rect(WIDTH * 0.35 * 1.35, HEIGHT * 0.285, WIDTH * 0.2, HEIGHT * 0.03) #pygame.Rect(650, 200, 140, 32)
        self.password_rect = pygame.Rect(WIDTH * 0.35 * 1.35, HEIGHT * 0.385, WIDTH * 0.2, HEIGHT * 0.03)# pygame.Rect(650, 300, 140, 32)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('grey')
        self.color1 =self.color_passive
        self.color = self.color_passive
        self.active = False
        self.active1 = False
        self.process()


    def process(self):
        global NowPage
        while NowPage == "Login":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        all_sprites.update(event) 
                    if self.login_rect.collidepoint(event.pos):
                        self.active = True
                    else:
                        self.active = False
                    if self.password_rect.collidepoint(event.pos):
                        self.active1 = True
                    else:
                        self.active1 = False
                if event.type == pygame.KEYDOWN:
                    if self.active is True and self.active1 == False:
                        if event.key == pygame.K_BACKSPACE: 
                            self.login = self.login[:-1]
                        elif event.key == pygame.K_KP_ENTER:
                            self.active = False
                        else:
                            self.login += event.unicode 
                    if self.active1 is True and self.active == False:
                        if event.key == pygame.K_BACKSPACE: 
                            self.password = self.password[:-1]
                        else:
                            self.password += event.unicode 

            if self.active and self.active1 == False:
                self.color = self.color_active
            else:
                self.color = self.color_passive

            if self.active1 and self.active == False:
                self.color1 = self.color_active
            else:
                self.color1 = self.color_passive 

            screen.fill(pygame.Color(247, 235, 235), pygame.Rect(WIDTH * 0.15, HEIGHT * 0.15, WIDTH * 0.70, HEIGHT))
            pygame.draw.rect(screen, self.color, self.login_rect, 2)
            pygame.draw.rect(screen, self.color1, self.password_rect, 2)

            screen.blit(self.font.render(self.login, True, pygame.Color("black")), (self.login_rect.x + 5, self.login_rect.y + 5))
            screen.blit(self.font.render(self.password, True, pygame.Color("black")), (self.password_rect.x + 5, self.password_rect.y + 5))
            screen.blit(self.font.render("Логин:", False, pygame.Color("black")), (WIDTH * 0.35 * 1.15, HEIGHT * 0.287))
            screen.blit(self.font.render("Пароль:", False, pygame.Color("black")), (WIDTH * 0.35 * 1.15, HEIGHT * 0.387))
            screen.blit(self.font1.render("Авторизация", False, pygame.Color("black")), (WIDTH * 0.35 * 1.2, HEIGHT * 0.2))
    
            self.login_rect.w = max(WIDTH * 0.09, self.font.render(self.login, True, pygame.Color("black")).get_width() + 10)
            self.password_rect.w = max(WIDTH * 0.09, self.font.render(self.password, True, pygame.Color("black")).get_width() + 10)

            pygame.display.flip()


class MAIN:
    def __init__(self):
        global online
        if client.set_up() is None:
            online = True
            Thread(target=client.start, daemon=True).start()
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
        global NowPage
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos):
                if functs[self.command] != None:
                    if 1 <= self.command <= 2:
                        Pages = {"Login": Login, "MainPage": MainPage}
                        NowPage = functs[self.command]
                        Pages[functs[self.command]]()
                    else:
                        functs[self.command]()


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()

    def set_up(self):
        try:
            self.socket.connect(
                ("127.0.0.1", 1234)
            )
        except ConnectionRefusedError:
            return "Sorry, server is offline"

        self.socket.setblocking(False)
        return

    async def listen_socket(self, listened_socket=None):
        global messages
        while True:
            data = await self.main_loop.sock_recv(self.socket, 2048)
            messages = data.decode('utf-8')

    def send_data(self, data=None):
        socket.send(self.socket, data.encode("utf-8"))

    async def main(self):
        await self.main_loop.create_task(self.listen_socket())


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Монополия")
    clock = pygame.time.Clock()
    client = Client()
    font = pygame.font.Font(None, 60)
    MAIN()