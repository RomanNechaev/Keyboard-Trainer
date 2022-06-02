import socket
from user import User
from application import trainer, keys
from curses.textpad import rectangle
from threading import Thread
import curses
from multiplayer import multiplayer_consts, clients_message
from typing import NoReturn


class Client:
    """Клиент для игры по сети"""

    def __init__(self, user: User, trainer: trainer) -> NoReturn:
        self.user = user
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "185.255.133.232"
        self.port = 1981
        self.trainer = trainer

    def run_client(self, stdscr) -> NoReturn:
        """ Запуск клиента для игры по сети


        Ключевые аргументы:
        stdscr -- главное окно
        """
        stdscr.clear()
        try:
            self.sock.connect((self.host, self.port))
        except Exception:
            raise Exception("не удалось подключиться к серверу :(")

        self.sock.send(f"{self.user.name}".encode())
        ready_message = self.sock.recv(1024).decode()
        stdscr.nodelay(1)
        window_coordinate = stdscr.getmaxyx()
        y, x = window_coordinate[0], window_coordinate[1]
        connection_count = 1
        while ready_message != "yes":
            if connection_count > 1:
                self.update_lobby(stdscr, ready_message, connection_count)
            else:
                self.create_lobby(stdscr, ready_message, connection_count)
            stdscr.getch()
            ready_message = self.sock.recv(1024).decode()
            connection_count += 1

        rdy_thread = Thread(
            target=self.print_readiness_other_player,
            args=(stdscr, multiplayer_consts.indent_from_username),
        )
        rdy_thread.start()

        while True:
            stdscr.nodelay(0)
            try:
                key = stdscr.get_wch()
            except curses.error:
                raise Exception("something wrong:(")
            color = curses.color_pair(1)
            if key in keys.KEY_R:
                self.sock.send("he".encode())
                stdscr.addstr(
                    6,
                    x // 2 - 18 + multiplayer_consts.indent_from_username + 1,
                    clients_message.ready,
                    color,
                )
                stdscr.getch()
                break

        self.check_thread_completion(rdy_thread)

        self.prepare_to_game(color, stdscr)
        self.trainer.wpm_test(stdscr)
        self.sock.send(f"{self.user.wpm} {self.user.name}".encode())
        data = self.sock.recv(1024)
        data2 = self.sock.recv(1024)
        self.print_result(data, data2)

        self.sock.close()

    @staticmethod
    def prepare_to_game(color, stdscr):
        """Подготовка окна к игре

        Ключевые аргументы:
        stdscr -- главное окно\n
        color -- цвет символа
        """
        stdscr.addstr(13, 13, clients_message.press_r, color)
        stdscr.getch()
        stdscr.clear()
        stdscr.refresh()
        stdscr.nodelay(0)
        stdscr.move(0, 0)

    @staticmethod
    def check_thread_completion(rdy_thread):
        """Проверка завершение работы потока


        Ключевые аргументы:
        rdy_thread -- поток
        """
        while True:
            if not rdy_thread.is_alive():
                break

    @staticmethod
    def print_result(data_fist_client, data_second_client) -> NoReturn:
        """Вывод результа от двух клиентов


        Ключевые аргументы:
        data_fist_client -- данные первого клиента\n
        data_second_client -- данные второго клиента
        """
        print(data_fist_client.decode())
        print(data_second_client.decode())

    @staticmethod
    def create_lobby(stdscr, message, connection_count) -> NoReturn:
        """Создание и отрисовка графического участка под игроков


        Ключевые аргументы:
        stdscr -- главное окно\n
        message -- сообщение от клиента\n
        connection_count -- количество подключенных игроков
        """
        window_coordinate = stdscr.getmaxyx()
        y, x = window_coordinate[0], window_coordinate[1]
        stdscr.addstr(3, x // 2 - 15, f"Комната 1. Игроков {connection_count}/2")
        rectangle(stdscr, 5, x // 2 - 20, 8, x - 10)
        stdscr.addstr(5 + connection_count, x // 2 - 18, message)
        stdscr.addstr(10, 5, clients_message.press_r)
        stdscr.addstr(12, 5, clients_message.press_two_space)

    @staticmethod
    def update_lobby(stdscr, message, connection_count) -> NoReturn:
        """Перерисовка графического участка под игроков


        Ключевые аргументы:
        stdscr -- главное окно\n
        message -- сообщение от клиента\n
        connection_count -- количество подключенных игроков
        """
        window_coordinate = stdscr.getmaxyx()
        y, x = window_coordinate[0], window_coordinate[1]
        stdscr.addstr(3, x // 2 - 15, f"Комната 1. Игроков {connection_count}/2")
        stdscr.addstr(5 + connection_count, x // 2 - 18, message)
        stdscr.addstr(5 + connection_count, x // 2 - 18, message)
        stdscr.addstr(10, 5, clients_message.press_r)
        stdscr.addstr(12, 5, clients_message.press_two_space)

    def print_readiness_other_player(self, stdscr, indent) -> NoReturn:
        """Ожидание и уведомление о готовности другого игрока


        Ключевые аргументы:
        stdscr -- главное окно\n
        indent -- отступ от юзернэйма игрока
        """
        stdscr.nodelay(0)
        while True:
            data = self.sock.recv(1024)
            if data:
                self.draw_readiness(stdscr, indent)
                break

    @staticmethod
    def draw_readiness(stdscr, indent) -> NoReturn:
        """Отрисовка готовности игрока


        Ключевые аргументы:
        stdscr -- главное окно\n
        indent -- отступ от юзернэйма игрока
        """

        window_coordinate = stdscr.getmaxyx()
        y, x = window_coordinate[0], window_coordinate[1]
        stdscr.addstr(
            7, x // 2 - 18 + indent + 1, clients_message.ready, curses.color_pair(1)
        )
        stdscr.refresh()
        stdscr.getch()
