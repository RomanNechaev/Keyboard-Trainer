import socket
from user import User
from application import Trainer
from curses.textpad import rectangle
import time
from threading import Thread
import curses
from application import KEYS


class Client:
    def __init__(self, user: User, trainer: Trainer):
        self.user = user
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"
        self.port = 1981
        self.trainer = trainer

    def run_client(self, stdscr):
        t = 0
        stdscr.clear()
        self.sock.connect((self.host, self.port))
        ready_message = self.sock.recv(1024).decode()
        stdscr.nodelay(1)
        window_coordinate = stdscr.getmaxyx()
        y, x = window_coordinate[0], window_coordinate[1]
        # self.create_lobby(stdscr)
        connection_count = 1
        while ready_message != "yes":
            if connection_count > 1:
                t = len(ready_message)
                self.update_lobby(stdscr, ready_message, connection_count)
            else:
                self.create_lobby(stdscr, ready_message, connection_count)
            stdscr.getch()
            ready_message = self.sock.recv(1024).decode()
            connection_count += 1

        # thread = Thread(target=self.wait_other_ready_player)
        # thread.start()
        ber = Thread(target=self.print_readiness_other_player, args=(stdscr, t))
        ber.start()

        # ej = Thread(target=self.wait_completion_another_thread, args=(thread))
        # ej.start()
        # Thread(target=self.print_readiness_other_player, args=(stdscr, thread, t)).start()

        while True:
            stdscr.nodelay(0)
            try:
                key = stdscr.get_wch()
            except curses.error:
                raise Exception("something wrong:(")
            color = curses.color_pair(1)
            if key in KEYS.KEY_R:
                self.sock.send("he".encode())
                stdscr.addstr(6, x // 2 - 18 + t + 1, 'RDY', color)
                stdscr.getch()
                break

        while True:
            if not ber.is_alive():
                break

        # break
        # if not thread.is_alive():
        #     stdscr.addstr(3, 3, "ye")
        #     stdscr.refresh()
        # #     stdscr.getch()
        # all_ready_message = self.sock.recv(1024)
        # while all_ready_message != "all clients ready":
        #     all_ready_message = self.sock.recv(1024)
        #     break
        stdscr.clear()
        stdscr.refresh()
        stdscr.nodelay(0)
        self.trainer.wpm_test(stdscr)

        self.sock.send(f"{self.user.wpm} {self.user.name}".encode())
        data = self.sock.recv(1024)
        print(data.decode())
        data2 = self.sock.recv(1024)
        print(data2.decode())

    def create_lobby(self, stdscr, message, connection_count):
        window_coordinate = stdscr.getmaxyx()
        y, x = window_coordinate[0], window_coordinate[1]
        stdscr.addstr(3, x // 2 - 15, f"Комната 1. Игроков {connection_count}/2")
        rectangle(stdscr, 5, x // 2 - 20, 8, x - 10)
        stdscr.addstr(5 + connection_count, x // 2 - 18, message)
        stdscr.addstr(10, 5, "Нажмите {R} для потверждения готовности к игре")

    def update_lobby(self, stdscr, message, connection_count):
        window_coordinate = stdscr.getmaxyx()
        y, x = window_coordinate[0], window_coordinate[1]
        stdscr.addstr(3, x // 2 - 15, f"Комната 1. Игроков {connection_count}/2")
        stdscr.addstr(5 + connection_count, x // 2 - 18, message)
        stdscr.addstr(5 + connection_count, x // 2 - 18, message)
        stdscr.addstr(10, 5, "Нажмите {R} для потверждения готовности к игре")

    def print_readiness_other_player(self, stdscr, t):
        stdscr.nodelay(0)
        while True:
            data = self.sock.recv(1024)
            if data:
                window_coordinate = stdscr.getmaxyx()
                y, x = window_coordinate[0], window_coordinate[1]
                stdscr.addstr(7, x // 2 - 18 + t + 1, 'RDY', curses.color_pair(1))
                stdscr.refresh()
                stdscr.getch()
                break

    def wait_other_ready_player(self):
        while True:
            data = self.sock.recv(1024)
            if data:
                break

    def wait_completion_another_thread(self, threader):
        while True:
            if not threader.is_alive():
                break
