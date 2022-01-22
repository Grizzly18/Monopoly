from socket import socket
import pygame
from win32api import GetSystemMetrics
from functions import *
from Socket import Socket
import asyncio
import time
import random
from PIL import Image, ImageDraw
from threading import Thread
from PIL import Image, ImageSequence

WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()
all_objs = []
functs = {None: None, 0: terminate, 1: "MainPage", 2: "Login"}
FPS = 120
messages, online, NowPage, login, players = "", False, "", "", ""
PiecPlayers = []


def crop(im, s):
    w, h = im.size
    k = w / s[0] - h / s[1]
    if k > 0: im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
    elif k < 0: im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
    return im.resize(s, Image.ANTIALIAS)


def prepare_mask(size, antialias = 2):
    mask = Image.new('L', (size[0] * antialias, size[1] * antialias), 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
    return mask.resize(size, Image.ANTIALIAS)



def circle_image(pict):
    im = Image.open(pict)
    size = (100, 100)
    im = crop(im, size)
    im.putalpha(prepare_mask(size, 4))
    im.save(pict[:-4] + "new" + ".png")


def resize_img(pict, w, h):
    img = Image.open(pict)
    new_img = img.resize((w, h))
    new_img.save(pict[:-4] + "2" + ".png", "PNG", optimize=True)


def translate(word):
    if (len(word) <= 0):
        return ""
    new_word = {}
    for i in word.split("!!!"):
        t = i.split('#')
        if (t == ['']):
            continue
        new_word[t[0]] = t[1].split('$')
    return new_word

def translate2(word):
    if (len(word) <= 0):
        return ""
    new_word = {}
    for i in word.split("!!!"):
        t = i.split('#')
        if (t == ['']):
            continue
        new_word[t[0]] = ''.join(t[1].split('$'))
    return new_word

def pilImageToSurface(pilImage):
    mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()

def loadGIF(filename):
    pilImage = Image.open(filename)
    frames = []
    if pilImage.format == 'GIF' and pilImage.is_animated:
        for frame in ImageSequence.Iterator(pilImage):
            pygameImage = pilImageToSurface(frame.convert('RGBA'))
            frames.append(pygameImage)
    else:
        frames.append(pilImageToSurface(pilImage))
    return frames


def Game(y, game, p):
    global players
    screen.fill(pygame.Color(219, 219, 219), pygame.Rect(WIDTH * 0.16, y, WIDTH * 0.68, 150))
    font1 = pygame.font.Font(None, 24)
    text = font1.render(f'Количество игроков: {len(p)}\\5', True, pygame.Color("black"))
    place = text.get_rect(center=(WIDTH * 0.23, y + 18))
    screen.blit(text, place)
    # circle_image("data/gray_user.png")
    for i in range(5):
        if (i < len(p)):
            try:
                all_objs.append(Button(load_image("gray_usernew.png"), (WIDTH * 0.25 + (i * 180), y + 80)))
                text2 = font1.render(f'{players[p[i]]}', True, pygame.Color("black"))
                place2 = text2.get_rect(center=(WIDTH * 0.25 + (i * 180), y + 140))
                screen.blit(text2, place2)
            except:
                pass
        else:
            all_objs.append(Button(load_image("join.png", colorkey=-1), (WIDTH * 0.25 + (i * 180), y + 80), game))

class MainPage:
    def __init__(self):
        global messages, client, NowPage, players
        NowPage = "MainPage"
        for i in all_objs:
            i.kill()
        for i in PiecPlayers:
            i.kill()
        screen.fill(pygame.Color(214, 210, 210))
        all_objs.append(Button(load_image("logo.png", colorkey=-1), (WIDTH / 100 * 16, HEIGHT / 100 * 7.5)))
        all_objs.append(Button(load_image("findgame.png", colorkey=-1), (WIDTH / 100 * 80, 65), 1))
        if (login == ""):
            all_objs.append(Button(load_image("login.png", colorkey=-1), (WIDTH / 100 * 93, 63), 2))
        else:
            all_objs.append(Button(load_image("logout.png", colorkey=-1), (WIDTH / 100 * 93, 63), 4))
        if online and login != '':
            client.send_data("check listgame")
            all_objs.append(Button(load_image("create.png", colorkey=-1), (WIDTH * 0.75, HEIGHT * 0.25), 5))
            time.sleep(0.5)
        if '&' in messages:
            players = translate2(messages.split("&")[1])
        self.all_games = translate(messages.split("&")[0])
        text = font.render(f'Ожидают игры', True, pygame.Color("black"))
        place = text.get_rect(center=(WIDTH * 0.3, HEIGHT * 0.25))
        screen.fill(pygame.Color(250, 242, 242), pygame.Rect(0, 0, WIDTH, HEIGHT / 100 * 15))
        screen.fill(pygame.Color(247, 235, 235), pygame.Rect(WIDTH * 0.15, HEIGHT * 0.15, WIDTH * 0.70, HEIGHT))
        if online and login == "":
            text2 = font.render(f'Необходимо войти в аккаунт', True, pygame.Color("black"))
            place2 = text.get_rect(center=(WIDTH // 2.4, HEIGHT // 2))
        elif (len(self.all_games) > 0):
            text2 = font.render(f'', True, pygame.Color("black"))
            place2 = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            i = 1
            for x in self.all_games:
                Game(HEIGHT * 0.12 + (i * 170), x, self.all_games[x])
                i += 1
        elif not online:
            text2 = font.render(f'Вы оффлайн', True, pygame.Color("black"))
            place2 = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        else:
            text2 = font.render(f'Игр пока что нет', True, pygame.Color("black"))
            place2 = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        while NowPage == "MainPage":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    all_sprites.update(event) 
            pygame.display.flip()
            screen.blit(text, place), screen.blit(text2, place2)
            all_sprites.draw(screen)
            all_sprites.update()
            clock.tick(FPS)


class Login:
    def __init__(self):
        global login
        self.password = ''
        for i in all_objs:
            i.kill()
        for i in PiecPlayers:
            i.kill()
        all_objs.append(Button(load_image("logo.png", colorkey=-1), (WIDTH / 100 * 16, HEIGHT / 100 * 7.5)))
        all_objs.append(Button(load_image("findgame.png", colorkey=-1), (WIDTH / 100 * 80, 65), 1))
        if (login == ""):
            all_objs.append(Button(load_image("login.png", colorkey=-1), (WIDTH / 100 * 93, 63), 2))
        else:
            all_objs.append(Button(load_image("logout.png", colorkey=-1), (WIDTH / 100 * 93, 63), 4))
        all_objs.append( Button(load_image("login.png", colorkey=-1), (WIDTH * 0.5, HEIGHT * 0.5), "LoginAc"))
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
        global NowPage, login
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
                            login = login[:-1]
                        elif event.key == pygame.K_KP_ENTER:
                            self.active = False
                        else:
                            login += event.unicode 
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

            screen.blit(self.font.render(login, True, pygame.Color("black")), (self.login_rect.x + 5, self.login_rect.y + 5))
            screen.blit(self.font.render(self.password, True, pygame.Color("black")), (self.password_rect.x + 5, self.password_rect.y + 5))
            screen.blit(self.font.render("Логин:", False, pygame.Color("black")), (WIDTH * 0.35 * 1.15, HEIGHT * 0.287))
            screen.blit(self.font.render("Пароль:", False, pygame.Color("black")), (WIDTH * 0.35 * 1.15, HEIGHT * 0.387))
            screen.blit(self.font1.render("Авторизация", False, pygame.Color("black")), (WIDTH * 0.35 * 1.2, HEIGHT * 0.2))
            self.login_rect.w = max(WIDTH * 0.09, self.font.render(login, True, pygame.Color("black")).get_width() + 10)
            self.password_rect.w = max(WIDTH * 0.09, self.font.render(self.password, True, pygame.Color("black")).get_width() + 10)
            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.flip()


class BlockPlayer(pygame.sprite.Sprite):
    def __init__(self, pos, player, command=None):
        global players
        super().__init__(all_sprites)
        self.image = load_image('BlockPlayer.png')
        self.rect = self.image.get_rect(center=pos)
        self.command = command


class TempPiece(pygame.sprite.Sprite):
    def __init__(self, image, pos, command=None):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.command = command
        self.pos = 0


class LOSEORWIN(pygame.sprite.Sprite):
    def __init__(self, image, pos, command=None):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.command = command
        self.pos = 0


class Piece(pygame.sprite.Sprite):
    def __init__(self, image, pos, command=None):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.command = command
        self.pos = 0

    def turn(self, turn):
        for i in range(turn):
            self.pos += 1
            if (self.pos > 40):
                self.pos -= 40
            if (self.pos <= 10):
                self.rect = self.rect.move(WIDTH * 0.03755, 0)
            elif (self.pos <= 20):
                self.rect = self.rect.move(0, HEIGHT * 0.0665)
            elif (self.pos <= 30):
                self.rect = self.rect.move(-(WIDTH * 0.03755), 0)
            elif (self.pos <= 40):
                self.rect = self.rect.move(0, -(HEIGHT * 0.0665))


class Board:
    def __init__(self, g, main=False):
        global NowPage, messages, PiecPlayers
        NowPage = "Game"
        resize_img("data/board.png", int(HEIGHT * 0.9), int(HEIGHT * 0.9))
        self.board = load_image('board2.png', colorkey=-1)
        self.pos_board = self.board.get_rect(center=(WIDTH * 0.60, HEIGHT // 2))
        for i in all_objs:
            i.kill()
        for i in PiecPlayers:
            i.kill()
        screen.fill(pygame.Color(33, 40, 43))
        screen.blit(self.board, self.pos_board)
        self.turn = messages
        client.send_data("check listgame")
        font1 = pygame.font.Font(None, 32)
        all_objs.append(Button(load_image("logout2.png", colorkey=-1), (80, HEIGHT * 0.05), f"ExitGame#{g}"))
        time.sleep(0.5)
        self.all_games = translate(messages.split("&")[0])
        if '&' in messages:
            self.players = (translate2(messages.split("&")[1]))
        pieces = ["red_piece.png", "blue_piece.png", "green_piece.png", "purple_piece.png", "orange_piece.png"]
        locks = ["red_lock.png", "blue_lock.png", "green_lock.png", "purple_lock.png", "orange_lock.png"]
        self.number = 0
        PiecPlayers = []
        for i in range(len(self.players)):
            try:
                all_objs.append(BlockPlayer((WIDTH * 0.20, HEIGHT * 0.15 + (i * 180)), self.all_games[g][i]))
                PiecPlayers.append(Piece(load_image(pieces[i], colorkey=-1), (WIDTH * 0.415, HEIGHT * 0.17 - (i * 5)), self.all_games[g][i]))
                if (players[self.all_games[g][i]] == login):
                    self.number = i
            except:
                pass
        if main:
            all_objs.append(Button(load_image("start.png", colorkey=-1), (WIDTH // 2, HEIGHT // 2), f"START#{g}"))
        start = True
        pos = PiecPlayers[self.number].rect
        money = [15000] * len(PiecPlayers)
        while NowPage == "Game":
            clock.tick(2)
            print(messages)
            if ("Player" in messages and "turn" in messages):
                p, t = messages.split(" ")[1], messages.split(" ")[3]
                PiecPlayers[int(p)].turn(int(t))
                if ("Player" in messages and "turn" in messages):
                    messages = ""
                client.send_data(f"check money {p}")
            if (PiecPlayers[self.number].rect != pos):
                pos = PiecPlayers[self.number].rect
                temp.kill()
                screen.fill(pygame.Color(33, 40, 43))
            if (messages == "BUY"):
                temp = BUY(load_image("buy.png"), (WIDTH // 2, HEIGHT // 2), self.number)
                all_objs.append(temp)
            if ("Player" in messages and "buy" in messages):
                p = int(messages.split(" ")[1])
                if p == self.number:
                    temp.kill()
                    screen.fill(pygame.Color(33, 40, 43))
                client.send_data(f"check money {p}")
                messages = ""
                all_objs.append(TempPiece(load_image(locks[p], colorkey=-1), (PiecPlayers[p].rect.x + 15, PiecPlayers[p].rect.y + 15)))
            if ("Player" in messages and "have" in messages):
                p, m = int(messages.split(" ")[1]), int(messages.split(" ")[3])
                money[p] = m
                if ("Player" in messages and "have" in messages):
                    messages = ""
            if (messages == "START GAME"):
                NowPage = ""
                time.sleep(0.5)
                Board(g, False)
            if (messages == "YOU LOSE"):
                client.send_data(f"ExitGame#{g}")
                all_objs.append(LOSEORWIN(load_image("Lose.png", colorkey=-1), (WIDTH // 2, HEIGHT // 2)))
            if (messages == "YOU WIN"):
                all_objs.append(LOSEORWIN(load_image("WIN.png", colorkey=-1), (WIDTH // 2, HEIGHT // 2)))
            if (messages == "UPDATE"):
                NowPage = ""
                time.sleep(0.5)
                Board(g, True)
            if (("TURN" in messages and int(messages.split(" ")[1]) == self.number) or (start and "TURN" in self.turn and int(self.turn.split(" ")[1]) == self.number)):
                # PiecPlayers[self.number].turn(random.randint(1, 6) + random.randint(1, 6))
                if ("TURN" in messages and int(messages.split(" ")[1]) == self.number):
                    messages = ""
                start = False
                temp = TURN(load_image("turn.png"), (WIDTH // 2, HEIGHT // 2), self.number)
                all_objs.append(temp)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    all_sprites.update(event) 
            screen.blit(self.board, self.pos_board)
            all_sprites.draw(screen)
            all_sprites.update()
            jj = 0
            for i in range(len(self.players)):
                try:
                    text2 = font1.render(f'{self.players[self.all_games[g][i]]}', True, pygame.Color(colors[i]))
                    place2 = text2.get_rect(center=(WIDTH * 0.20, HEIGHT * 0.15 + (i * 180)))
                    screen.blit(text2, place2)
                    text3 = font1.render(f'{money[jj]}$', True, pygame.Color("white"))
                    place3 = text3.get_rect(center=(WIDTH * 0.20, HEIGHT * 0.20 + (i * 180)))
                    screen.blit(text3, place3)
                    jj += 1
                except:
                    pass
            colors = ["red", "blue", "green", "purple", "orange"]
            pygame.display.flip()


class MAIN:
    def __init__(self):
        global online, NowPage
        if client.set_up() is None:
            online = True
            Thread(target=client.start, daemon=True).start()
        all_objs.append(Button(load_image("logo.png", colorkey=-1), (WIDTH / 100 * 16, HEIGHT / 100 * 7.5)))
        all_objs.append(Button(load_image("findgame.png", colorkey=-1), (WIDTH / 100 * 80, 65), 1))
        all_objs.append(Button(load_image("login.png", colorkey=-1), (WIDTH / 100 * 93, 63), 2))
        Button(load_image("exit.png"), (WIDTH - 25, 15), 0)
        screen.fill(pygame.Color(214, 210, 210))
        MainPage()


class BUY(pygame.sprite.Sprite):
    def __init__(self, image, pos, number):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.number = number

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos):
                client.send_data(f"BUY {self.number}")


class AUCTION(pygame.sprite.Sprite):
    def __init__(self, image, pos, number):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.number = number

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos):
                client.send_data(f"auction {self.number}")

class TURN(pygame.sprite.Sprite):
    def __init__(self, image, pos, number):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.number = number

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos):
                turn = random.randint(1, 6) + random.randint(1, 6)
                # turn = 1
                # PiecPlayers[self.number].turn(turn)
                client.send_data(f"Player {self.number} turn {turn}")


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos, command=None):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.command = command

    def update(self, *args):
        global NowPage, login
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos):
                if self.command == 5 and online:
                    client.send_data("create game")
                    time.sleep(0.5)
                    Board(messages, True)
                    # NowPage = ""
                    # NowPage = "MainPage"
                    # MainPage()
                elif self.command == 4:
                    login = ""
                    NowPage = ""
                    NowPage = "MainPage"
                    MainPage()
                elif self.command != None and  "ExitGame" in str(self.command):
                    client.send_data(self.command)
                    NowPage = ""
                    NowPage = "MainPage"
                    MainPage()
                elif self.command != None and "game" in str(self.command) and "START" not in str(self.command):
                    client.send_data(f"join#game#{str(self.command)}")
                    Board(str(self.command))
                    # NowPage = ""
                    # NowPage = "MainPage"
                    # MainPage()
                elif self.command != None and "START" in str(self.command):
                    client.send_data(self.command)
                elif self.command != None and online and str(self.command) == "LoginAc": 
                    NowPage = "MainPage"
                    client.send_data(f"LOGIN {login}")
                    MainPage()
                elif self.command in functs and functs[self.command] != None:
                    if 1 <= self.command <= 2:
                        Pages = {"Login": Login, "MainPage": MainPage}
                        NowPage = functs[self.command]
                        Pages[functs[self.command]]()
                    else:
                        functs[self.command]()


def load():
    global NowPage
    gifFrameList = loadGIF("data/load.gif")
    currentFrame = 0
    while NowPage == "":
        clock.tick(4)
        if NowPage == "":
            rect = gifFrameList[currentFrame].get_rect(center = (WIDTH // 2, HEIGHT // 2))
            screen.blit(gifFrameList[currentFrame], rect)
            currentFrame = (currentFrame + 1) % len(gifFrameList)
            pygame.display.flip()

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
    Thread(target=load, daemon=True).start()
    client = Client()
    font = pygame.font.Font(None, 60)
    MAIN()