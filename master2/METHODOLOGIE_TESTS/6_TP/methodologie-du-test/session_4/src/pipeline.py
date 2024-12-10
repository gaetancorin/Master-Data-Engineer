from typing import Any
from data import TuplePropreSansPrix
from provider import Provider
from cleaner import Cleaner
from trainer import Trainer, ModelSaver
from model_comparator import ModelComparator


class Pipeline:
    provider: Provider
    cleaner: Cleaner
    trainer: Trainer
    model_comparator: ModelComparator
    saver: ModelSaver

    def __init__(
        self,
        provider: Provider,
        cleaner: Cleaner,
        trainer: Trainer,
        saver: ModelSaver,
        model_comparator: ModelComparator,
    ):
        self.cleaner = cleaner
        self.provider = provider
        self.trainer = trainer
        self.saver = saver
        self.model_comparator = model_comparator

    def get_data_and_train_model(self, logger) -> None:
        logger.info(f"Start Train Function")
        tuples = self.provider.get()
        cleaned_tuples = self.cleaner.clean(tuples)
        model = self.trainer.train(cleaned_tuples)
        self.saver.save(model)
        self.model_comparator.add_metadata(model.metadata)
        logger.info(f"Done Train Function")

    def predict(self, tuples: list[TuplePropreSansPrix], logger) -> Any:
        logger.info(f"Start Predict Function")
        best_models_metadata = self.model_comparator.get_best_model()
        logger.info(f"Best Model choose is {best_models_metadata.name}")
        model = self.saver.get_model_from_metadata(best_models_metadata)
        result = model.predict(tuples)
        logger.info(f"Done Predict Function")
        return result
