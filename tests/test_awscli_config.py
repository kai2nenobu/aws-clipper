
from io import StringIO

from awscli_config import _convert


def test_empty():
    input_yaml = StringIO("")
    output = StringIO()
    _convert(input_yaml, output)
    assert output.getvalue() == ""


def test_only_default_profile():
    input_yaml = StringIO("""\
profiles:
  default:
    region: us-east-1
""")
    output = StringIO()
    _convert(input_yaml, output)
    assert output.getvalue() == """\
[default]
region = us-east-1

"""


def test_single_named_profile():
    input_yaml = StringIO("""\
profiles:
  my:
    region: us-east-1
""")
    output = StringIO()
    _convert(input_yaml, output)
    assert output.getvalue() == """\
[profile my]
region = us-east-1

"""
