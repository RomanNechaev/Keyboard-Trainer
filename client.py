import socket
from application import App
from user import User
from user import UserState
from application import TextGenerator


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "localhost"
    port = 1488
    sock.connect((host, port))
    ready_message = sock.recv(1024).decode()
    while ready_message != "yes":
        print(ready_message)
        ready_message = sock.recv(1024).decode()
    name = input("Введите имя")
    user = User.User(UserState.State.PLAYING, name)
    text_generator = TextGenerator.TextGenerator(1, "konstitucia-rf.txt")
    a = App.Application(user, text_generator)

    a.run_app()

    sock.send(f"{a.user.wpm}{name}".encode())
    data = sock.recv(1024)
    print(data.decode())
    data2 = sock.recv(1024)
    print(data2.decode())


if __name__ == "__main__":
    client()

# TODO: добавить комнаты
# TODO: начать игру по готовности юзеров
