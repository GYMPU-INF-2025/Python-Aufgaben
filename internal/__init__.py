import random

from internal.tasks import Task
from internal.result import Result
from aufgaben import aufgabe_1, aufgabe_2, aufgabe_3, aufgabe_4, aufgabe_5, aufgabe_6, aufgabe_7, aufgabe_8, aufgabe_9, \
    aufgabe_10, aufgabe_11, aufgabe_12, aufgabe_13, aufgabe_14

def good_aufgabe_4(val_1: int, val_2: int) -> int:
    return val_1 + val_2


def good_aufgabe_5(val_1: int, val_2: int) -> int:
    return val_1 * val_2

def good_aufgabe_6(val_1: int) -> str:
    return str(val_1)

def good_aufgabe_7(val_1: int, val_2: int, val_3: str, val_4: bool) -> list[str | bool | int]:
    return [val_1, val_2, val_3, val_4]

def good_aufgabe_8(val_1: list[int]) -> list[int | str]:
    val_1[0] = "OPG"
    val_1[2] = "OPG"
    return val_1

def good_aufgabe_9(val_1: list[int]) -> list[int | str]:
    val_1.append("OPG")
    return val_1

def good_aufgabe_10(val_1: int) -> bool:
    return val_1 % 2 == 0

def good_aufgabe_11(val_1: int) -> None:
    if val_1 > 0:
        print("Nina")
    elif val_1 == 0:
        print("Elijah")
    else:
        print("Ludwig")


def good_aufgabe_12() -> None:
    i = 1
    while i < 6:
        print(i)
        i += 1

def good_aufgabe_13(val_1: list[str]) -> None:
    for x in val_1:
        print(x)

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
    Task(
        func=aufgabe_4,
        good_func=good_aufgabe_4,
        val_1=random.randint(0, 10000),
        val_2=random.randint(0, 10000),
    ),
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
    ),
    Task(
        func=aufgabe_7,
        good_func=good_aufgabe_7,
        val_1=random.randint(0, 10000),
        val_2=random.randint(0, 10000),
        val_3=str(random.randint(0, 10000) + random.randint(0, 10000)),
        val_4=(random.randint(0, 100) % 2) == 0
    ),
    Task(
        func=aufgabe_8,
        good_func=good_aufgabe_8,
        val_1=[random.randint(0, 100) for _ in range(10)]
    ),
    Task(
        func=aufgabe_9,
        good_func=good_aufgabe_9,
        val_1=[random.randint(0, 100) for _ in range(10)]
    ),
    Task(
        func=aufgabe_10,
        good_func=good_aufgabe_10,
        val_1=random.randint(0,1000000)
    ),
    Task(
        func=aufgabe_11,
        good_func=good_aufgabe_11,
        val_1=random.randint(-1,1)
    ),
    Task(
        func=aufgabe_12,
        good_func=good_aufgabe_12
    ),
    Task(
        func=aufgabe_13,
        good_func=good_aufgabe_13,
        val_1=[f"Nummer {x}" for x in range(5)]
    ),
    Task(
        func=aufgabe_14,
        result=Result(
            expect_stdout=True,
            return_value_type=str
        )
    ),
]

