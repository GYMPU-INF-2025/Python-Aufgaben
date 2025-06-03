from __future__ import annotations


def aufgabe_1() -> None:
    """Geben Sie etwas in die Konsole aus.

    Hilfe:
    https://www.w3schools.com/python/python_strings.asp
    """
    print("test")


def aufgabe_2() -> None:
    """Geben Sie genau "GYMPU" in die Konsole aus.

    Hilfe:
    https://www.w3schools.com/python/python_strings.asp
    """
    print("GYMPU")


def aufgabe_3() -> int:
    """Geben Sie in dieser Funktion irgendeine Zahl zurück."""
    return 123

def aufgabe_4(val_1: int, val_2: int) -> int:
    """Schreiben Sie eine Funktion welche 2 Zahlen zusammenaddiert.

    Hilfe:
    https://www.w3schools.com/python/python_operators.asp
    """
    return val_1 + val_2


def aufgabe_5(val_1: int, val_2: int) -> int:
    """Schreiben Sie eine Funktion welche 2 Zahlen zusammen multipliziert.

    Hilfe:
    https://www.w3schools.com/python/python_operators.asp
    """
    return val_1 * val_2


def aufgabe_6(val_1: int) -> str:
    """Schreiben Sie eine Funktion welche die gegebene Zahl in einen String wandelt.

    Hilfe:
    https://www.w3schools.com/python/python_casting.asp
    """
    return str(val_1)


def aufgabe_7(val_1: int, val_2: int, val_3: str, val_4: bool) -> list[str | bool | int]:
    """Schreiben Sie eine Funktion welche die gegebenen Argumente zu einer Liste hinzufügt und diese zurückgibt.
    Achten Sie auf die richtige Reihenfolge!

    Hilfe:
    https://www.w3schools.com/python/python_lists.asp
    """
    return [val_1, val_2, val_3, val_4]

def aufgabe_8(val_1: list[int]) -> list[int | str]:
    """Schreiben Sie eine Funktion welche das 1. und das 3. Objekt aus der Liste zu dem String "OPG" ändert.

    Hilfe:
    Listen fangen nicht bei 1, sondern bei 0 anzuzählen!
    https://www.w3schools.com/python/python_lists_change.asp
    """
    val_1[0] = "OPG"
    val_1[2] = "OPG"
    return val_1

def aufgabe_9(val_1: list[int]) -> list[int | str]:
    """Schreiben Sie eine Funktion welche einen String "OPG" zu der Liste hinzufügt.

    Hilfe:
    https://www.w3schools.com/python/python_lists_add.asp
    """
    val_1.append("OPG")
    return val_1

def aufgabe_10(val_1: int) -> bool:
    """Schreiben Sie eine Funktion welche zurückgibt, ob eine Zahl glatt durch 2 teilbar ist.

    Hilfe:
    https://www.w3schools.com/python/python_operators.asp (Modulus)
    https://www.w3schools.com/python/python_booleans.asp
    """
    return val_1 % 2 == 0

def aufgabe_11(val_1: int) -> None:
    """Schreiben Sie eine Funktion die "Nina" in die Konsole ausgibt, wenn die Zahl größer als 0 ist, und "Ludwig" ausgibt, wenn die Zahl kleiner 0 ist.
    Wenn die Zahl 0 ist, soll die Funktion "Elijah" in die Konsole ausgeben.

    Hilfe:
    https://www.w3schools.com/python/python_conditions.asp
    """
    if val_1 > 0:
        print("Nina")
    elif val_1 == 0:
        print("Elijah")
    else:
        print("Ludwig")


def aufgabe_12() -> None:
    """Schreiben Sie eine Funktion welche nacheinander jede Zahl zwischen 1 und 5 in die Konsole ausgibt.

    Benutzten sie einen while loop.

    Hilfe:
    https://www.w3schools.com/python/python_while_loops.asp
    """
    i = 1
    while i < 6:
        print(i)
        i += 1


def aufgabe_13(val_1: list[str]) -> None:
    """Schreiben Sie eine Funktion welche jedes Objekt aus der Liste in die Konsole ausgibt.

    Benutzten sie einen for loop.

    Hilfe:
    https://www.w3schools.com/python/python_for_loops.asp
    """
    for x in val_1:
        print(x)

def aufgabe_14() -> str:
    """Schreiben Sie eine Funktion welche eingabe des Nutzers über die Konsole verlangt,
    und diese Eingabe dann in die Konsole ausgibt. Außerdem soll die Funktion die Eingabe des Nutzers zurückgeben
    
    Hilfe:
    https://www.w3schools.com/python/python_user_input.asp
    """
    var = input("Input: ")
    print(var)
    return var
    
    