from typing import Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder, FunctionTransformer
import pickle


class Cleaner:
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop(labels=["date", "transaction_id", "client_id"], axis=1)
        valid_values = ["legit", "fraud", "high_risk", "low_risk"]
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df = df[df["amount"].notna() & (df["amount"] >= 1)]
        df = df[df["label"].isin(valid_values)]
        return df.dropna(axis=0)


class PandasProvider:
    def get(self) -> pd.DataFrame:
        raise NotImplementedError


class PandasCsvProvider(PandasProvider):
    def __init__(self, path: str) -> None:
        self.path: str = path

    def get(self) -> pd.DataFrame:
        return pd.read_csv(self.path)


class Metadata:
    def __init__(self, accuracy: float):
        self.accuracy: float = accuracy

    def __str__(self) -> str:
        return f"Metadata({self.accuracy})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Metadata):
            return NotImplemented
        return self.accuracy == other.accuracy

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Metadata):
            return NotImplemented
        return self.accuracy < other.accuracy

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, Metadata):
            return NotImplemented
        return self == other or self < other

    def __gt__(self, other: Any) -> bool:
        return not self <= other

    def __ge__(self, other: Any) -> bool:
        return not self < other


class Model:
    def __init__(self, pipeline: Pipeline, metadata: Metadata):
        self.pipeline: Pipeline = pipeline
        self.metadata: Metadata = metadata


def hash_transform(x: pd.DataFrame) -> pd.DataFrame:
    return x.map(hash)


class Trainer:
    def train(self, df: pd.DataFrame) -> Model:
        # Separate features and target
        X = df[["product_id", "amount"]]
        y = df["label"]

        # Label encode the target variable
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y)

        # Preprocessing steps
        preprocessor = ColumnTransformer(
            transformers=[
                # For product_id: hash it or apply custom logic (ensure it's treated as DataFrame here)
                (
                    "product_id",
                    FunctionTransformer(hash_transform),
                    ["product_id"],
                ),
                # Scale amount
                ("amount", StandardScaler(), ["amount"]),
            ],
            remainder="drop",
        )

        # Define the model
        model = RandomForestClassifier(random_state=42)

        # Create the pipeline
        pipeline = Pipeline(
            steps=[("preprocessor", preprocessor), ("classifier", model)]
        )

        # Split data for training and evaluation
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=20, stratify=y
        )

        # Train the pipeline
        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        return Model(pipeline=pipeline, metadata=Metadata(accuracy))


class Saver:
    def save(self, model: Model, filepath: str) -> None:
        raise NotImplementedError

    def load(self, filepath: str) -> None | Model:
        raise NotImplementedError


class FilesystemSaver(Saver):
    def save(self, model: Model, filepath: str) -> None:
        with open(filepath, "wb") as file:
            pickle.dump(model, file)

    def load(self, filepath: str) -> None | Model:
        try:
            with open(filepath, "rb") as file:
                model = pickle.load(file)
            return model  # type: ignore
        except FileNotFoundError:
            return None


class ModelComparatorAndSaver:
    def __init__(self, saver: Saver):
        self.saver: Saver = saver

    def save(self, model: Model, filepath: str) -> None:
        self.saver.save(model, filepath)

    def load(self, filepath: str) -> None | Model:
        return self.saver.load(filepath)

    def overwrite_if_better_than_reference(self, model: Model) -> None:
        previous = self.load("model.pkl")
        if previous is None:
            print("No previous model")
            self.save(model, "model.pkl")
        else:
            if previous.metadata <= model.metadata:
                print(
                    f"previous: {previous.metadata} <= new: {model.metadata}, saving new model"
                )
                self.save(model, "model.pkl")
            else:
                print(
                    f"previous: {previous.metadata} > new: {model.metadata}, ignoring new model"
                )
