from . import convert


def main() -> None:
    import sys

    convert(sys.stdin, sys.stdout)


if __name__ == "__main__":
    main()
