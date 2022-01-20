from re import S
from telnetlib import SE
from Socket import Socket
import asyncio


def translate(word):
    new_word = ""
    for i in word:
        new_word += f"{i}#{'$'.join(word[i])}!!!"
    return new_word

class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        self.games = {}
        self.users = []
        self.Logs = {}

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
                print(self.games)
                if data.decode('utf-8') == "create game":
                    self.games[f"game-{str(listened_socket)}"] = [str(listened_socket)]
                    await self.main_loop.sock_sendall(listened_socket, f"game-{str(listened_socket)}".encode('utf-8'))
                elif "join#game" in data.decode('utf-8'):
                    t = data.decode('utf-8')
                    print(t)
                    self.games[t.split("#")[2]].append(str(listened_socket))
                elif "check listgame" == data.decode('utf-8'):
                    await self.main_loop.sock_sendall(listened_socket, f"{translate(self.games)}&{translate(self.Logs)}".encode('utf-8'))
                elif "LOGIN" in data.decode('utf-8'):
                    self.Logs[listened_socket] = data.decode('utf-8').split(" ")[1]
                elif "ExitGame" in data.decode('utf-8'):
                    self.games[data.decode('utf-8').split("#")[1]].remove(listened_socket)
                elif "START" in data.decode('utf-8'):
                    game = data.decode('utf-8').split("#")[1]
                    print(self.games[game])

            except ConnectionResetError:
                print("Client removed")
                self.users.remove(listened_socket)
                try:
                    del self.Logs[listened_socket]
                    for i in self.games:
                        for j in self.games[i]:
                            if j not in self.users:
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
            self.main_loop.create_task(self.listen_socket(user_socket))

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())


if __name__ == '__main__':
    server = Server()
    server.set_up()

    server.start()
