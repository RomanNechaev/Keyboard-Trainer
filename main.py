from application import app
import argparse
from user import User
from user import UserState


def main():
    script_name = "Keyboard trainer"
    script = argparse.ArgumentParser(
        usage=f"{script_name} [-n WORDS COUNT] [-u USER_NAME] [-o OS]"
    )

    script.add_argument(
        "-n", "--words", default=10, type=int, help="Enter a words count for training"
    )

    script.add_argument(
        "-u", "--user", default="bublic", type=str, help="Enter a username"
    )

    script.add_argument(
        "-f", "--file", default="konstitucia-rf", type=str, help="Enter a filename for parse"
    )

    args = script.parse_args()

    user = User.User(UserState.State.PLAYING, args.user)

    a = app.Application(args.words, user, args.file)

    a.run_app()


if __name__ == "__main__":
    main()
