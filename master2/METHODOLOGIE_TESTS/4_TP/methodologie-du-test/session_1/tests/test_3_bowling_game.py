from src.session_1.tp_3_bowling_game import Game
import pytest


@pytest.fixture
def game():
    return Game()


# def test_rolls_5(game) -> None:
#     assert False
