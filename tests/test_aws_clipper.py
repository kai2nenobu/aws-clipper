from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import Any

import pytest

from aws_clipper import convert


def all_test_data() -> list[Any]:
    """Read from input yaml and expected config from "data" directory."""
    data_dir = Path(__file__).parent / "data"
    yamls = data_dir.glob("**/*.yaml")

    def param(yaml_file: Path) -> Any:
        test_name = yaml_file.name
        ini = yaml_file.with_suffix(".ini")
        enc = "utf-8"
        return pytest.param(yaml_file.read_text(encoding=enc), ini.read_text(encoding=enc), id=test_name)

    return [param(yaml_file) for yaml_file in yamls]


@pytest.mark.parametrize("input_yaml, expected_config", all_test_data())
def test_data(input_yaml: str, expected_config: str) -> None:
    input = StringIO(input_yaml)
    output = StringIO()
    convert(input, output)
    assert output.getvalue() == expected_config
