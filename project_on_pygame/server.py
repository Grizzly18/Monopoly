from re import S
from telnetlib import SE
from Socket import Socket
import asyncio
import time
import random


def translate(word):
    new_word = ""
    for i in word:
        new_word += f"{i}#{'$'.join(word[i])}!!!"
    return new_word


class Card:
    def __init__(self, price, sold, h, com=None):
        self.price, self.sold, self.h, self.com = price, sold, h, com
        self.owner = ""


g = {}
chance = {'Заплатить всем 30': 'pay all 30'}




class Player:
    def __init__(self):
        self.money = 15000
        self.cards = []
        self.pos = 0



class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        self.games = {}
        self.users = []
        self.Logs = {}
        self.sock = {}
        self.turns = {}
        self.play = {}

    def set_up(self):
        self.socket.bind(("127.0.0.1", 1234))

        self.socket.listen(5)
        self.socket.setblocking(False)
        print("Server is listening")

    async def send_data(self, data=None):
        for user in self.users:
            await self.main_loop.sock_sendall(user, data)


    async def listen_socket(self, listened_socket=None):
        if not listened_socket:
            return

        while True:
            try:
                data = await self.main_loop.sock_recv(listened_socket, 2048)
                # В ИГРЕ
                if (data.decode('utf-8') != 'create game' and data.decode('utf-8') != 'check listgame' and "check money" not in data.decode('utf-8')):
                    for i in self.games:
                        if str(listened_socket) in self.games[i] and i in self.turns:
                            # Обработчик
                            if "BUY" in data.decode('utf-8'):
                                p = int(data.decode('utf-8').split(" ")[1])
                                current_card = g[i][self.play[i][p].pos]
                                if current_card.price <= self.play[i][p].money: 
                                    self.play[i][p].money -= current_card.price
                                    current_card.owner = p
                                    for j in self.games[i]:
                                        await self.main_loop.sock_sendall(self.sock[j], f"Player {p} buy {self.play[i][p].pos}".encode('utf-8'))
                                    time.sleep(0.5)
                            if "auction" in data.decode('utf-8'):
                                pass
                            if "prison" in data.decode('utf-8'):
                                pass
                            if ("Player" in data.decode('utf-8') and "turn" in data.decode('utf-8')):
                                print("YES")
                                for j in self.games[i]:
                                    await self.main_loop.sock_sendall(self.sock[j], data)
                                time.sleep(0.5)
                                p, t = data.decode('utf-8').split(" ")[1], data.decode('utf-8').split(" ")[3]
                                p, t = int(p), int(t)
                                self.play[i][p].pos += t
                                if (self.play[i][p].pos > 40):
                                    self.play[i][p].pos -= 40
                                    self.play[i][p].money += 2000
                                current_card = g[i][self.play[i][p].pos]
                                if (current_card.com == None and current_card.owner == ''):
                                    await self.main_loop.sock_sendall(listened_socket, f"BUY".encode('utf-8'))
                                elif (current_card.com == "money"):
                                    self.play[i][p].money += random.randint(100, 500)
                                elif (current_card.com == "diamond"):
                                    self.play[i][p].money += random.randint(500, 1000)
                                elif (current_card.com == "jackpot"):
                                    self.play[i][p].money += random.randint(-500, 500)
                                time.sleep(0.5)

                            self.turns[i] = len(self.games[i]) % (self.turns[i] + 1)
                            for j in self.games[i]:
                                await self.main_loop.sock_sendall(self.sock[j], f"TURN {self.turns[i]}".encode('utf-8'))

                # НЕ В ИГРЕ
                print(data.decode('utf-8'))
                if "check money" in data.decode('utf-8'):
                    p = int(data.decode('utf-8').split(" ")[2])
                    await self.main_loop.sock_sendall(listened_socket, f"Player {str(p)} have {str(self.play[i][p].money)}".encode('utf-8'))
                if data.decode('utf-8') == "create game":
                    self.games[f"game-{str(listened_socket)}"] = [str(listened_socket)]
                    await self.main_loop.sock_sendall(listened_socket, f"game-{str(listened_socket)}".encode('utf-8'))
                elif "join#game" in data.decode('utf-8'):
                    t = data.decode('utf-8')
                    self.games[t.split("#")[2]].append(str(listened_socket))
                elif "check listgame" == data.decode('utf-8'):
                    await self.main_loop.sock_sendall(listened_socket, f"{translate(self.games)}&{translate(self.Logs)}".encode('utf-8'))
                elif "LOGIN" in data.decode('utf-8'):
                    self.Logs[str(listened_socket)] = data.decode('utf-8').split(" ")[1]
                elif "ExitGame" in data.decode('utf-8'):
                    self.games[data.decode('utf-8').split("#")[1]].remove(str(listened_socket))
                    if len(self.games[data.decode('utf-8').split("#")[1]]) < 1:
                        del self.games[data.decode('utf-8').split("#")[1]]
                elif "START" in data.decode('utf-8'):
                    game = data.decode('utf-8').split("#")[1]
                    self.turns[game] = 0 
                    g[game] = [Card(-1, -1, -1, com='start'), Card(600, 300, 150), Card(-1, -1, -1, com="chance"), Card(600, 300, 150), Card(-1, -1, -1, com='money'),
                               Card(2000, 1000, 700), Card(1000, 500, 200), Card(-1, -1, -1, com="chance"), Card(1000, 500, 200), Card(1200, 600, 250), Card(-1, -1, -1, com='prison'), 
                               Card(1400, 700, 350), Card(1500, 750, 400), Card(1400, 700, 350), Card(1400, 700, 350), Card(2000, 1000, 700), Card(1800, 900, 500), Card(-1, -1, -1, com='chance'),
                               Card(1800, 900, 500), Card(2000, 1000, 700), Card(-1, -1, -1, com='jackpot'), Card(2200, 1100, 850), Card(-1, -1, -1, com="chance"), Card(2200, 1100, 850),
                               Card(2400, 1200, 900), Card(2000, 1000, 700), Card(2600, 1300, 1000), Card(2600, 1300, 1000), Card(1500, 750, 400), Card(2800, 1400, 1100), Card(-1, -1, -1, com='police'),
                               Card(3000, 1500, 1200), Card(3000, 1500, 1200), Card(-1, -1, -1, com="chance"), Card(3200, 1600, 1300), Card(2000, 1000, 700), Card(-1, -1, -1, com="diamond"),
                               Card(3500, 1750, 1400), Card(-1, -1, -1, com="chance"), Card(4000, 2000, 1600)]
                    self.play[game] = []
                    for p in self.games[game]:
                        self.play[game].append(Player())
                    for p in self.games[game]:
                        await self.main_loop.sock_sendall(self.sock[p], f"START GAME".encode('utf-8'))
                    time.sleep(0.5)
                    for p in self.games[game]:
                        await self.main_loop.sock_sendall(self.sock[p], f"TURN {self.turns[game]}".encode('utf-8'))

            except ConnectionResetError:
                print("Client removed")
                self.users.remove(listened_socket)
                del self.sock[str(listened_socket)]
                try:
                    del self.Logs[str(listened_socket)]
                    self.temp = []
                    for t in self.users:
                        self.temp.append(str(t))
                    for i in self.games:
                        for j in self.games[i]:
                            if j not in self.temp:
                                self.games[i].remove(j)
                        if len(self.games[i]) < 1:
                            del self.games[i]
                    return
                except:
                    pass
                return

    async def accept_sockets(self):
        while True:
            user_socket, address = await self.main_loop.sock_accept(self.socket)
            print(f"User <{address[0]}> connected!")

            self.users.append(user_socket)
            self.sock[str(user_socket)] = user_socket
            self.main_loop.create_task(self.listen_socket(user_socket))

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())


if __name__ == '__main__':
    server = Server()
    server.set_up()

    server.start()
