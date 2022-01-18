from markupsafe import re
from Socket import Socket
import asyncio


def translate(word):
    new_word = ""
    for i in range(len(word)):
        new_word = f"{i};{'$'.join(word[i])} "
    return new_word

class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()
        self.games = {}
        self.users = []

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
                if data.decode('utf-8') == "create game":
                    self.games[f"game-{listened_socket}"] = [listened_socket]
                elif "join game" in data.decode('utf-8'):
                    print(data[2][5:], data[2][4:])
                    self.games[data[2][5:]].append(listened_socket)
                elif "check listgame" == data.decode('utf-8'):
                    await self.main_loop.sock_sendall(listened_socket, translate(self.games).encode('utf-8'))
                else:
                    await self.send_data(data)
                print(self.games)

            except ConnectionResetError:
                print("Client removed")
                self.users.remove(listened_socket)
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
