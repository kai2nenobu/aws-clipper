from io import StringIO
from pathlib import Path

import pytest

from awscli_config import _convert


def all_test_data():
    """Read from input yaml and expected config from "data" directory."""
    data_dir = Path(__file__).parent / "data"
    yamls = data_dir.glob("**/*.yaml")
    def param(yaml_file: Path):
        test_name = yaml_file.name
        ini = yaml_file.with_suffix(".ini")
        enc = "utf-8"
        return pytest.param(yaml_file.read_text(encoding=enc), ini.read_text(encoding=enc), id=test_name)

    return [param(yaml_file) for yaml_file in yamls]


@pytest.mark.parametrize("input_yaml, expected_config", all_test_data())
def test_data(input_yaml: str, expected_config: str):
    input = StringIO(input_yaml)
    output = StringIO()
    _convert(input, output)
    assert output.getvalue() == expected_config
