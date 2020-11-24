import sys

from bot.knotbot import Knotbot


def main() -> None:
    bot = Knotbot()
    bot.run(sys.argv[1])


if __name__ == "__main__":
    main()
