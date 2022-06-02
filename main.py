from application import app
from application import text_generator
from db import orm
import argparse
from user import User
from user import UserState
import socket


def parse_args():
    global args
    script_name = "Keyboard trainer"
    script = argparse.ArgumentParser(
        usage=f"{script_name} [-n WORDS COUNT] [-u USER_NAME] [-o OS]"
    )

    script.add_argument(
        "-n", "--words", default=10, type=int, help="Enter a words count for training"
    )

    script.add_argument(
        "-t", "--top", action='store_true', help="Show top players"
    )

    script.add_argument(
        "-r", "--result", type=str, help="Check your last results"
    )

    script.add_argument(
        "-u", "--user", default="bublic", type=str, help="Enter a username"
    )

    script.add_argument(
        "-f", "--file", default="konstitucia-rf", type=str, help="Enter a filename for parse"
    )

    args = script.parse_args()


def sql():
    global a
    if args.user != "bublic":
        orm.insert(a.user)

    if args.top:
        orm.show_top()

    if args.result:
        orm.show_result(args.result)


def main():
    global a
    parse_args()
    if args.top or args.result:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("185.255.133.232", 1989))
        app_enable = False
        if args.top:
            sock.send("top".encode())
        else:
            sock.send(f"{args.result}".encode())
        top = sock.recv(65534)
        print(top.decode())
    else:
        app_enable = True

    if app_enable:
        user = User.User(UserState.State.PLAYING, args.user)
        text_gen = text_generator.TextGenerator("konstitucia-rf.txt")
        a = app.Application(user, text_gen, args.words)
        a.run_app()


# sql()


if __name__ == "__main__":
    main()
