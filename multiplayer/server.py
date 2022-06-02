import socket
from threading import Thread
import time
from collections import namedtuple
from typing import NoReturn
from typing import List


class Server:
    """Сервер для мультиплеерной игры в клавиатурный тренажер"""

    def __init__(self, players_number) -> NoReturn:
        self.serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.stat = []
        self.thread_list = []
        self.players_number = players_number
        self.ready_players = []
        self.user_names = {}

    def start_server(self) -> NoReturn:
        """Запуск сервера и обработка клиентов"""
        self.serv_socket.bind(("localhost", 1981))
        exit_listener = Thread(target=self.notify_client_about_result)
        while True:
            self.serv_socket.listen(5)
            client_sock, client_address = self.serv_socket.accept()
            if client_sock:
                self.clients.append((client_sock, client_address))
                thread = Thread(args=(client_sock, client_address), target=self.handle)
                self.thread_list.append(thread)
                user_name = client_sock.recv(1024).decode()
                client_sock.send(f"Игрок {user_name} подключился".encode())
                self.user_names[client_sock] = user_name
            if len(self.thread_list) == self.players_number:
                client_without_self = self.clients.copy()
                client_without_self.remove((client_sock, client_address))
                for cl in client_without_self:
                    cl[0].send(
                        f"Игрок {self.user_names[client_sock]} подключился".encode()
                    )
                    client_sock.send(
                        f"Игрок {self.user_names[cl[0]]} подключился".encode()
                    )
                self.notify_clients(message="yes")
                for cle in self.clients:
                    ready_thread = Thread(
                        target=self.wait_ready_message, args=(cle[0],)
                    )
                    ready_thread.start()
                    Client_ready = namedtuple(
                        "Client_ready", ["thread", "client", "dispatched"]
                    )
                    self.ready_players.append(
                        Client_ready(
                            ready_thread,
                            client=cle[0],
                            dispatched={"dispatched": False},
                        )
                    )
                while True:
                    if (
                            all(not x.thread.is_alive() for x in self.ready_players)
                            and self.all_client_dispatched()
                    ):
                        break
                    for ready_player in self.ready_players:
                        if (
                                not ready_player.thread.is_alive()
                                and not ready_player.dispatched["dispatched"]
                        ):
                            for client in self.clients:
                                if client[0] != ready_player.client:
                                    client[0].send("ready".encode())
                                    ready_player.dispatched["dispatched"] = True
                time.sleep(0.01)
                self.start_game(self.thread_list)
                exit_listener.start()

    @staticmethod
    def wait_ready_message(cl: socket) -> NoReturn:
        """Ожидание ответа от клиента

        Ключевые аргументы:
        cl -- сокет клиента
        """
        while True:
            ready = cl.recv(1024)
            if ready:
                break

    def handle(self, connection: socket, client_address: str) -> NoReturn:
        """Собирает данные юзера после завершенной игры


        Ключевые аргументы:
        connection -- сокет клиента\n
        client_address -- ip клиента
        """
        raw_data = connection.recv(1024)
        data = raw_data.decode().split(" ")
        User_stat = namedtuple("User_stat", ["wpm", "ip", "name"])
        self.stat.append(User_stat(wpm=data[0], ip=client_address, name=data[1]))
        connection.send(f"Результаты:".encode())

    def notify_client_about_result(self) -> NoReturn:
        """Уведомление клиентов о результатах игры"""
        while True:
            if len(self.thread_list) != 0:
                flag = False
                for n in self.thread_list:
                    if n.is_alive():
                        flag = True
                if flag is False and len(self.thread_list) == len(self.clients):
                    self.notify_clients(self.get_stat())
                    break

    @staticmethod
    def start_game(thread_list: List[Thread]) -> NoReturn:
        """Запускает потоки обработки игры от разных клиентов

        Ключевые аргументы:
        thread_list -- список потоков для обработки клиентов
        """
        for thread in thread_list:
            thread.start()

    def get_stat(self) -> str:
        """Возврщает статистику об завершенной игре"""
        result = ""
        self.stat.sort(key=lambda x: x.wpm)
        for user in self.stat:
            result += f"{user.ip} aka {user.name} набрал {user.wpm}\n"
        return result

    def notify_clients(self, message: str) -> NoReturn:
        """Отправляем уведомление всем клиентам сервера


        Ключевые аргументы:
        message -- уведомление
        """
        for client in self.clients:
            client[0].send(message.encode())
            time.sleep(0.1)

    def all_client_dispatched(self) -> bool:
        """Проверяет, что все клиенты отправили уведомление о готовности начать игру"""
        return all(
            ready_player.dispatched["dispatched"] for ready_player in self.ready_players
        )


if __name__ == "__main__":
    t = Server(players_number=2)
    t.start_server()
