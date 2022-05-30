import socket
from threading import Thread
import time
from collections import namedtuple


class Server:
    def __init__(self, players_number):
        self.serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.stat = []
        self.thread_list = []
        self.players_number = players_number
        self.ready_players = []

    def start_server(self):
        self.serv_socket.bind(("127.0.0.1", 1981))
        exit_listener = Thread(target=self.get_results)
        while True:
            self.serv_socket.listen(5)
            client_sock, client_addres = self.serv_socket.accept()
            if client_sock:
                self.clients.append((client_sock, client_addres))
                thread = Thread(args=(client_sock, client_addres), target=self.handle)
                self.thread_list.append(thread)
                client_sock.send(f"Игрок {client_addres} подключился".encode())

            if len(self.thread_list) == self.players_number:
                client_without_self = self.clients.copy()
                client_without_self.remove((client_sock, client_addres))
                for cl in client_without_self:
                    cl[0].send(f"Игрок {client_addres} подключился".encode())
                    client_sock.send(f"Игрок {cl[1]} подключился".encode())
                self.notify_clients(message="yes")
                for cle in self.clients:
                    ready_thread = Thread(target=self.wait_ready_message, args=(cle[0],))
                    ready_thread.start()
                    Client_ready = namedtuple('Client_ready', ['thread', 'client', 'dispatched'])
                    self.ready_players.append(
                        Client_ready(ready_thread, client=cle[0], dispatched={'dispatched': False}))
                while True:
                    if all(not x.thread.is_alive() for x in self.ready_players):
                        break
                    for ready_player in self.ready_players:
                        if not ready_player.thread.is_alive() and not ready_player.dispatched['dispatched']:
                            for client in self.clients:
                                if client[0] != ready_player.client:
                                    client[0].send("ready".encode())
                                    ready_player.dispatched['dispatched'] = True
                print(2)
                # TODO: Не проверял, возможно баги в коде с 42-49
                time.sleep(0.1)
                # self.notify_clients(message="all clients ready")
                self.start_game(self.thread_list)
                exit_listener.start()

    @staticmethod
    def wait_ready_message(cl):
        while True:
            ready = cl.recv(1024)
            if ready:
                break

    def handle(self, connection, client_addres):
        raw_data = connection.recv(1024)
        data = raw_data.decode().split(" ")
        wpm = data[0]
        name = data[1]
        User_stat = namedtuple('User_stat', ['wpm', 'ip', 'name'])
        self.stat.append(User_stat(wpm, client_addres, name))

        connection.send(f"WPM of your opponent's".encode())

    def get_results(self):
        while True:
            if len(self.thread_list) != 0:
                k = False
                for n in self.thread_list:
                    if n.is_alive():
                        k = True
                if k is False and len(self.thread_list) == len(self.clients):
                    for client in self.clients:
                        client[0].send(self.get_stat().encode())
                    break

    @staticmethod
    def start_game(thread_list):
        for thread in thread_list:
            thread.start()

    def get_stat(self):
        result = ""
        self.stat.sort(key=lambda x: x.wpm)
        for user in self.stat:
            result += f"{user.ip} aka {user.name} набрал {user.wpm}\n"
        return result

    def notify_clients(self, message):
        for client in self.clients:
            client[0].send(message.encode())
            time.sleep(0.1)


if __name__ == "__main__":
    t = Server(players_number=2)
    t.start_server()

# TODO: добавить сохранение информации
# TODO: корректное восстановление инфы при рестарте сервера
# TODO: рефакторинг
