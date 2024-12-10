import json
from logging import Logger

from data import TupleSale


class Provider:
    def get(self) -> list[TupleSale]:
        raise NotImplementedError


class JsonProvider(Provider):
    file_path: str
    logger: Logger

    def __init__(self, file_path: str, logger: Logger):
        self.file_path = file_path
        self.logger = logger

    def get(self) -> list[TupleSale]:
        with open(self.file_path, "r") as file:
            data = json.load(file)
        return [TupleSale(**item) for item in data]
