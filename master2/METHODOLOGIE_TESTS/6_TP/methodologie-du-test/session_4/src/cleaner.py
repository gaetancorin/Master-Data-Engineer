from logging import Logger

from data import TupleSale, TuplePropre, BienType


class Cleaner:
    logger: Logger

    def __init__(self, logger: Logger):
        self.logger = logger

    def clean(self, input_data: list[TupleSale]) -> list[TuplePropre]:
        cleaned_data = []
        for item in input_data:
            try:
                prix = int(item.prix)
                surface = int(item.surface)
                pieces = int(item.pieces)
                type_str = item.type_bien.lower()
                if (
                    prix == 0
                    or surface == 0
                    or pieces == 0
                    or (type_str != "appartement" and type_str != "maison")
                ):
                    continue
                type_bien = (
                    BienType.Appartement
                    if type_str == "appartement"
                    else BienType.Maison
                )

                cleaned_data.append(
                    TuplePropre(
                        surface=surface,
                        pieces=pieces,
                        type_bien=type_bien,
                        prix=prix,
                    )
                )
            except (ValueError, TypeError):
                continue
        self.logger.info(f"Cleaner to keep {len(cleaned_data)} pieces of data out of {len(input_data)}")
        return cleaned_data
