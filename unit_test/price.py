import pytest
from matchers.price import match

cases = [
    ("", ()),
    ("", ()),
    ("", ())
]

@pytest.mark.parametrize("test_input,expected", cases)
def test_eval(test_input, expected):
    assert match(test_input) == expected

