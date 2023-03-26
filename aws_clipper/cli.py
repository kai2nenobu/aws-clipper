from __future__ import annotations

import argparse
import sys


def cli_main(argv: list[str]) -> int:
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
    args = parser.parse_args(argv)

    from . import convert

    convert(args.input, args.output)
    return 0


def main() -> None:  # pragma: no cover
    sys.exit(cli_main(sys.argv[1:]))


if __name__ == "__main__":
    main()
