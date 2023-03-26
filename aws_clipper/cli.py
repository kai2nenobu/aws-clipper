from __future__ import annotations

import argparse
import sys


def _print_version() -> None:
    from . import __version__

    print(__version__)


def cli_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="aws-clipper", description="Dump AWS CLI config from a simple YAML file.")
    parser.add_argument("--version", action="store_true", help="show version")
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
    if args.version:
        _print_version()
        return 0

    from . import convert

    convert(args.input, args.output)
    return 0


def main() -> None:  # pragma: no cover
    sys.exit(cli_main(sys.argv[1:]))


if __name__ == "__main__":
    main()
