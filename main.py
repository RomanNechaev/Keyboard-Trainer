from application import App
import argparse
from user import User
from user import UserState
from application import TextGenerator


def main():
    script_name = "Keyboard trainer"
    script = argparse.ArgumentParser(
        usage=f"{script_name} [-n WORDS COUNT] [-u USER_NAME] [-f filename]"
    )

    script.add_argument(
        "-n", "--words", default=10, type=int, help="Enter a words count for training"
    )

    script.add_argument(
        "-u", "--user", default="bublic", type=str, help="Enter a username"
    )

    script.add_argument(
        "-f", "--file", default="konstitucia-rf.txt", type=str, help="Enter a filename for parse"
    )

    args = script.parse_args()

    user = User.User(UserState.State.PLAYING, args.user)
    text_generator = TextGenerator.TextGenerator(args.file)
    a = App.Application(user, text_generator, args.words)

    a.run_app()


if __name__ == "__main__":
    main()
