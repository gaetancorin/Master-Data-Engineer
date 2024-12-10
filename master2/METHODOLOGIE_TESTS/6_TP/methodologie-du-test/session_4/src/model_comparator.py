import json
from trainer import Metadata


class ModelComparator:
    def add_metadata(self, metadata: Metadata) -> None:
        raise NotImplementedError

    def get_best_model(self) -> Metadata:
        raise NotImplementedError


class InMemoryModelComparator(ModelComparator):
    def __init__(self) -> None:
        self.metadata_list: list[Metadata] = []

    def add_metadata(self, metadata: Metadata) -> None:
        self.metadata_list.append(metadata)

    def get_best_model(self) -> Metadata:
        if not self.metadata_list:
            raise ValueError("No models have been added.")
        self.metadata_list = sorted(self.metadata_list, key=lambda meta: meta.score, reverse=True)
        return self.metadata_list[-1]


class FilesystemModelComparator(ModelComparator):
    def __init__(self, wrapped: InMemoryModelComparator, json_path: str, logger):
        self.wrapped = wrapped
        self.json_path = json_path
        self.logger = logger
        self._load_metadata()

    def _load_metadata(self) -> None:
        try:
            with open(self.json_path, "r") as file:
                data = json.load(file)
                for item in data:
                    self.wrapped.add_metadata(Metadata(name=item["name"], score=item["score"]))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def _save_metadata(self) -> None:
        with open(self.json_path, "w") as file:
            json.dump(
                [{"name": m.name, "score": m.score} for m in self.wrapped.metadata_list],
                file,
            )

    def add_metadata(self, metadata: Metadata) -> None:
        self.wrapped.add_metadata(metadata)
        self._save_metadata()

    def get_best_model(self) -> Metadata:
        return self.wrapped.get_best_model()
