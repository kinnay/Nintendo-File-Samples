
from generators import Generator


def main() -> None:
    for cls in Generator.__subclasses__():
        instance = cls()
        instance.generate()


if __name__ == "__main__":
    main()
