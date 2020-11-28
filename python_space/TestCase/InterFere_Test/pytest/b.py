import pytest

@pytest.mark.parametrize(("a", "b", "expected"), [
    [1, 2, 3],
    [10, 11, 21],
    [1, 1, 1],
])
def test_1(a, b, expected):
    assert a + b == expected

if __name__ == "__main__":
    pytest.main(["-v"])