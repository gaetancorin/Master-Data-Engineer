import logging

import pytest

from cleaner import Cleaner
from data import TuplePropre, TupleSale, BienType
import pandas as pd


@pytest.fixture
def cleaner() -> Cleaner:
    return Cleaner(logging.getLogger())

def test_noop(cleaner: Cleaner) -> None:
    assert [] == cleaner.clean([])

def test_eq() -> None:
    assert TuplePropre(
        type_bien=BienType.Maison, prix=100, surface=200, pieces=6
    ) == TuplePropre(type_bien=BienType.Maison, prix=100, surface=200, pieces=6)

def test_cleaner_good_tuplesale(cleaner: Cleaner) -> None:
    tuplesale = TupleSale(surface=10,pieces=1,prix=10,type_bien="appartement")
    tupleclean = cleaner.clean([tuplesale])
    assert [TuplePropre(type_bien=BienType.Appartement, prix=10, surface=10, pieces=1)] == tupleclean

def test_cleaner_bad_insert(cleaner: Cleaner) -> None:
    tuplesale = TupleSale(surface=10,pieces=1,prix=10,type_bien="bas_insert")
    tupleclean = cleaner.clean([tuplesale])
    assert [TuplePropre(type_bien=BienType.Appartement, prix=10, surface=10, pieces=1)] != tupleclean

def test_cleaner_not_receive_table(cleaner: Cleaner) -> None:
    tuplesale = TupleSale(surface=10,pieces=1,prix=10,type_bien="appartement")
    with pytest.raises(TypeError, match="'TupleSale' object is not iterable"):
        cleaner.clean(tuplesale)

def test_cleaner_string_parameter_instead_of_int(cleaner: Cleaner) -> None:
    tuplesale = TupleSale(surface="string",pieces=1,prix=10,type_bien="appartement")
    tupleclean = cleaner.clean([tuplesale])
    assert tupleclean == []