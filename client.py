import socket
from user import User
from application import Trainer
from curses.textpad import rectangle
import time


class Client:
    def __init__(self, user: User, trainer: Trainer):
        self.user = user
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"
        self.port = 1488
        self.trainer = trainer

    def run_client(self, stdscr):
        stdscr.clear()
        self.sock.connect((self.host, self.port))
        ready_message = self.sock.recv(1024).decode()
        stdscr.nodelay(1)
        # self.create_lobby(stdscr)
        connection = 1
        while ready_message != "yes":
            if connection > 1:
                self.update_lobby(stdscr, ready_message, connection)
            else:
                self.create_lobby(stdscr, ready_message, connection)
            stdscr.getch()
            ready_message = self.sock.recv(1024).decode()
            connection += 1
        #TODO: добавить кнопку с готовностью, отправить сообщение о готовности серверу
        # обновлять готовность другого игрока, когда поток(проверки готовности) закончит свою работу
        time.sleep(30)
        stdscr.clear()
        stdscr.refresh()
        stdscr.nodelay(0)
        time.sleep(5)
        self.trainer.wpm_test(stdscr)

        self.sock.send(f"{self.user.wpm} {self.user.name}".encode())
        data = self.sock.recv(1024)
        print(data.decode())
        data2 = self.sock.recv(1024)
        print(data2.decode())

    def create_lobby(self, stdscr, message, connection):
        window_coordinate = stdscr.getmaxyx()
        y, x = window_coordinate[0], window_coordinate[1]
        stdscr.addstr(3, x // 2 - 15, f"Комната 1. Игроков {connection}/2")
        rectangle(stdscr, 5, x // 2 - 20, 8, x - 10)
        stdscr.addstr(5 + connection, x // 2 - 18, message)

    def update_lobby(self, stdscr, message, connection):
        window_coordinate = stdscr.getmaxyx()
        y, x = window_coordinate[0], window_coordinate[1]
        stdscr.addstr(3, x // 2 - 15, f"Комната 1. Игроков {connection}/2")
        stdscr.addstr(5 + connection, x // 2 - 18, message)

    def wait_other_ready_player(self):
        pass
    # TODO: другой поток, который ждет готовности от первого юзера
# if __name__ == "__main__":
#     selfclient()

# TODO: добавить  2 комнату
# TODO: начать игру по готовности юзеров
