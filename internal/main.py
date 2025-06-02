import logging.config
import json
import pathlib
import random

from internal.tasks import Task
from internal.result import Result
from aufgaben import aufgabe_1, aufgabe_2, aufgabe_3, aufgabe_4, aufgabe_5, aufgabe_6


ROOT_PATH = pathlib.Path(__file__).parent


def good_aufgabe_5(val_1: int, val_2: int) -> int:
    return val_1 + val_2


def good_aufgabe_6(val_1: int, val_2: int) -> int:
    return val_1 * val_2


tasks = [
    Task(
        func=aufgabe_1,
        result=Result(
            expect_stdout=True,
        ),
    ),
    Task(
        func=aufgabe_2, result=Result(expect_stdout=True, expected_error_msg="GYMPU\n")
    ),
    Task(func=aufgabe_3, result=Result(return_value_type=int)),
    Task(func=aufgabe_4, result=Result(return_value=4)),
    Task(
        func=aufgabe_5,
        good_func=good_aufgabe_5,
        val_1=random.randint(0, 10000),
        val_2=random.randint(0, 10000),
    ),
    Task(
        func=aufgabe_6,
        good_func=good_aufgabe_6,
        val_1=random.randint(0, 10000),
        val_2=random.randint(0, 10000),
    ),
]

if __name__ == "__main__":
    with (ROOT_PATH / "logging.json").open() as f:
        logging.config.dictConfig(json.load(f))
    for task in tasks:
        task.run_task()
    pass
