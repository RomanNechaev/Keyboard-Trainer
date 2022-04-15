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
        "-n", "--words", default=20, type=int, help="Enter a words count for training"
    )

    script.add_argument(
        "-u", "--user", default="bublic", type=str, help="Enter a username"
    )

    script.add_argument(
        "-o",
        "--os",
        default="Windows",
        type=str,
        help="Enter the name of your operating system",
    )

    args = script.parse_args()

    user = User.User(UserState.State.PLAYING, args.os)

    a = app.Application(args.words, user)

    a.run_app()


if __name__ == "__main__":
    main()
