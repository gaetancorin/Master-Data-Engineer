#!/usr/bin/env python
from pipeline import (
    PandasCsvProvider,
    Cleaner,
    Trainer,
    ModelComparatorAndSaver,
    PandasProvider,
    FilesystemSaver,
)


def main(provider: PandasProvider, saver: ModelComparatorAndSaver) -> None:
    cleaner = Cleaner()
    trainer = Trainer()

    df = provider.get()
    df = cleaner.clean(df)
    model = trainer.train(df)
    saver.overwrite_if_better_than_reference(model)


if __name__ == "__main__":
    main(
        provider=PandasCsvProvider("transactions-fair.csv"),
        saver=ModelComparatorAndSaver(FilesystemSaver()),
    )
