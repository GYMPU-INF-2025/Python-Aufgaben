import logging.config
import json
import pathlib

from internal import tasks

ROOT_PATH = pathlib.Path(__file__).parent

if __name__ == "__main__":
    with (ROOT_PATH / "logging.json").open() as f:
        logging.config.dictConfig(json.load(f))
    for task in tasks:
        task.run_task()
    pass
