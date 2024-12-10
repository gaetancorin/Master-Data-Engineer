#!/usr/bin/env python
import logging
import os
from dotenv import load_dotenv
from configuration import configure_logger
from data import BienType, TuplePropreSansPrix
from pipeline import Pipeline
from provider import JsonProvider
from cleaner import Cleaner
from model_comparator import FilesystemModelComparator, InMemoryModelComparator
from trainer import ScikitLearnTrainer, ScikitModelSaver
import argparse


def train() -> None:
    
    pipeline.get_data_and_train_model(logger)


def predict() -> None:
    data = [
        TuplePropreSansPrix(surface=138, pieces=2, type_bien=BienType.Appartement),
        TuplePropreSansPrix(surface=138, pieces=3, type_bien=BienType.Appartement),
        TuplePropreSansPrix(surface=138, pieces=2, type_bien=BienType.Maison),
        TuplePropreSansPrix(surface=138, pieces=3, type_bien=BienType.Maison),
    ]
    predictions = pipeline.predict(data, logger)

    for input, output in zip(data, predictions):
        logger.info(f"Prediction for {input} is {output}")


if __name__ == "__main__":
    load_dotenv()
    configure_logger(os.getenv("LOGGER_DSN", ""))
    logging.debug("starting application")
    logger = logging.getLogger(__name__)

    logging.debug("Instantiating JsonProvider")
    provider = JsonProvider("data/input/prix.json", logger)
    logging.debug("Instantiating Cleaner")
    cleaner = Cleaner(logger)
    logging.debug("Instantiating ScikitLearnTrainer")
    trainer = ScikitLearnTrainer(test_size=0.2, random_state=50, logger=logger)
    logging.debug("Instantiating ScikitModelSaver")
    saver = ScikitModelSaver(save_path="data/output/models", logger=logger)
    logging.debug("Instantiating FilesystemModelComparator")
    comparator = FilesystemModelComparator(
        wrapped=InMemoryModelComparator(), json_path="data/output/comparatif.json", logger=logger
    )
    logging.debug("Instantiating Pipeline")
    pipeline = Pipeline(provider, cleaner, trainer, saver, comparator)

    parser = argparse.ArgumentParser(description="A script to train or predict models.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Commands")
    
    train_parser = subparsers.add_parser("train", help="Train a model")
    train_parser.set_defaults(func=train)

    predict_parser = subparsers.add_parser(
        "predict", help="Predict using a trained model"
    )
    predict_parser.set_defaults(func=predict)

    args = parser.parse_args()
    args.func()

    logging.debug("ending application")
