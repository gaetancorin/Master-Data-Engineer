import logging
from pathlib import Path
from urllib.parse import urlparse


def configure_logger(logger_dsn: str) -> None:
    parsed_logger_config = urlparse(logger_dsn)
    if parsed_logger_config.scheme != "file":
        raise ValueError(
            f"configure logger only supports `file://` configuration, {parsed_logger_config.scheme} given"
        )

    log_file = parsed_logger_config.netloc + parsed_logger_config.path

    queries = parsed_logger_config.query.split("&")
    level = logging.INFO
    level_as_str = "INFO"

    log_file_path = Path(log_file)
    log_file_path.parents[0].mkdir(parents=True, exist_ok=True)
    log_handlers: list[logging.Handler] = [logging.FileHandler(log_file)]

    for query in queries:
        if "=" not in query:
            query += "="
        (key, value) = query.split("=", 2)
        match key:
            case "level":
                level_as_str = value
                level = level_from_value(level_as_str)
            case "console":
                log_handlers.append(logging.StreamHandler())
            case _:
                raise ValueError(
                    f"unknown query configuration {key} only `level` supported"
                )

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s: %(message)s",
        handlers=log_handlers,
    )
    logging.info(f"logging with configuration: {log_file} at level: {level_as_str}")


def level_from_value(value: str) -> int:
    match value.upper():
        case "CRITICAL":
            return logging.CRITICAL
        case "FATAL":
            return logging.FATAL
        case "ERROR":
            return logging.ERROR
        case "WARN":
            return logging.WARN
        case "WARNING":
            return logging.WARNING
        case "INFO":
            return logging.INFO
        case "DEBUG":
            return logging.DEBUG
        case _:
            return logging.NOTSET
