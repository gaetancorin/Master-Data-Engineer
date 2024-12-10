from enum import Enum, auto
from typing import Any


class TupleSale:
    prix: str
    surface: str
    pieces: str
    type_bien: str

    def __init__(self, prix: str, surface: str, pieces: str, type_bien: str):
        self.prix = prix
        self.surface = surface
        self.pieces = pieces
        self.type_bien = type_bien


class BienType(Enum):
    Appartement = auto()
    Maison = auto()


class TuplePropre:
    surface: int
    pieces: int
    type_bien: BienType
    prix: int

    def __init__(self, prix: int, surface: int, pieces: int, type_bien: BienType):
        self.prix = prix
        self.surface = surface
        self.pieces = pieces
        self.type_bien = type_bien

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TuplePropre):
            raise NotImplementedError
        return (
            other.pieces == self.pieces
            and other.surface == self.surface
            and other.type_bien == self.type_bien
            and other.prix == self.prix
        )


class TuplePropreSansPrix:
    surface: int
    pieces: int
    type_bien: BienType

    def __init__(self, surface: int, pieces: int, type_bien: BienType):
        self.surface = surface
        self.pieces = pieces
        self.type_bien = type_bien

    def __str__(self) -> str:
        return f"TupleSansPrix(surface: {self.surface}, pieces: {self.pieces}, type: {self.type_bien})"
