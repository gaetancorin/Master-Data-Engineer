import logging

from cleaner import Cleaner
from data import TupleSale
from model_comparator import ModelComparator, InMemoryModelComparator
from pipeline import Pipeline
from provider import Provider
from trainer import ScikitLearnTrainer, ModelSaver, Model

logger = logging.getLogger()


class MockProvider(Provider):
    def __init__(self, data: list[TupleSale]):
        self.data: list[TupleSale] = data

    def get(self) -> list[TupleSale]:
        return self.data


class MockSaver(ModelSaver):
    def save(self, model: Model) -> None:
        pass


def make_pipeline(
    provider: Provider | None = None,
    saver: ModelSaver | None = None,
    model_comparator: ModelComparator | None = None,
) -> Pipeline:
    if provider is None:
        provider = MockProvider(
            [
                TupleSale(prix="100000", surface="100", type_bien="maison", pieces="4"),
                TupleSale(prix="100000", surface="100", type_bien="maison", pieces="4"),
                TupleSale(prix="100000", surface="100", type_bien="maison", pieces="4"),
                TupleSale(prix="100000", surface="100", type_bien="maison", pieces="4"),
                TupleSale(prix="100000", surface="100", type_bien="maison", pieces="4"),
            ]
        )
    if saver is None:
        saver = MockSaver()
    if model_comparator is None:
        model_comparator = InMemoryModelComparator()
    return Pipeline(
        provider,
        Cleaner(logger),
        ScikitLearnTrainer(0.2, 2, logger),
        saver,
        model_comparator,
    )


def test_comparator_gets_something_from_real_model() -> None:
    comparator = InMemoryModelComparator()
    pipeline = make_pipeline(model_comparator=comparator)
    pipeline.get_data_and_train_model()
    assert comparator.metadata_list[0] is not None


def test_pipeline() -> None:
    make_pipeline(
        provider=MockProvider(
            [TupleSale(prix="100000", surface="100", type_bien="maison", pieces="4")]
        )
    )
