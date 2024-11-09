import pytest
from src.session_1.tp_0_calculatrice import Calculatrice


@pytest.fixture
def calc():
    """Fixture pour initialiser une instance de la calculatrice."""
    return Calculatrice()


def test_add(calc):
    assert False


# def test_subtract(calc):
#     assert False

# def test_multiply(calc):
#     assert False

# def test_divide(calc):
#     assert False
