from pathlib import Path

from pytest import CaptureFixture

from aws_clipper.cli import cli_main


def test_empty_input(capsys: CaptureFixture[str]) -> None:
    empty_input = Path(__file__).parent / "data/empty.yaml"
    cli_main([str(empty_input)])
    out, _ = capsys.readouterr()
    assert out == ""
