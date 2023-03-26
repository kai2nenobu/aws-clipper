def main() -> None:
    import sys

    from . import convert

    convert(sys.stdin, sys.stdout)


if __name__ == "__main__":
    main()
