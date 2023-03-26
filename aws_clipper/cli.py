from __future__ import annotations


def main() -> None:
    import argparse
    import sys

    from . import convert

    parser = argparse.ArgumentParser(prog="aws-clipper", description="Dump AWS CLI config from a simple YAML file.")
    parser.add_argument(
        "input",
        metavar="FILE",
        nargs="?",
        type=argparse.FileType("r", encoding="utf-8"),
        default=sys.stdin,
        help="input YAML file",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        nargs="?",
        type=argparse.FileType("w", encoding="utf-8"),
        default=sys.stdout,
        help="output config file",
    )
    args = parser.parse_args(sys.argv[1:])

    convert(args.input, args.output)


if __name__ == "__main__":
    main()
