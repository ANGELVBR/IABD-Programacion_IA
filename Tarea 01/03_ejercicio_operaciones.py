#!/usr/bin/env python3
"""Problema 3. Trabajo con conjuntos.

Escribe una función que reciba dos listas de enteros y devuelva un diccionario
con la siguiente información (ES OBLIGATORIO USAR CONJUNTOS PARA CALCULARLOS)

1. La intersección de ambos conjuntos (elementos comunes).
2. La unión de ambos conjuntos (todos los elementos sin duplicados).
3. La diferencia simétrica (elementos que están en uno u otro conjunto, pero no en ambos).
"""

import sys


def parse_numbers(text: str) -> set[int]:
    """Turn a text such as '1, 2, 3' or '1 2 3' into a set of integers."""
    text = text.replace(",", " ")
    numbers = set()
    for piece in text.split():
        try:
            numbers.add(int(piece))
        except ValueError:
            raise SystemExit(f"Error: '{piece}' is not an integer number.")
    return numbers


def set_operations(first: list[int], second: list[int]) -> dict[str, set[int]]:
    """Return the intersection, union and symmetric difference of both lists.

    Sets are mandatory here: they remove duplicates and provide the three
    operations in a single step.
    """
    first_set = set(first)
    second_set = set(second)

    return {
        "intersection": first_set & second_set,
        "union": first_set | second_set,
        "symmetric_difference": first_set ^ second_set,
    }


def show_result(result: dict[str, set[int]], first: list[int], second: list[int]) -> None:
    """Print the three sets in a readable, sorted way."""
    print(f"First list : {sorted(first)}")
    print(f"Second list: {sorted(second)}")
    print("-" * 50)

    labels = {
        "intersection": "Intersection (common elements)",
        "union": "Union (all, no duplicates)",
        "symmetric_difference": "Symmetric difference (one or the other)",
    }

    for key, label in labels.items():
        values = sorted(result[key])
        print(f"{label}:")
        print(f"    {values}   ({len(values)} elements)")

    print("-" * 50)

def main() -> None:
    arguments = sys.argv[1:]

    if len(arguments) >= 2:
        first = parse_numbers(arguments[0])
        second = parse_numbers(arguments[1])
    elif not arguments:
        print("Type the first list (e.g. 1, 2, 3, 4)")
        first = parse_numbers(input("> "))
        print("Type the second list (e.g. 3, 4, 5, 6)")
        second = parse_numbers(input("> "))
    else:
        print(
            f"Usage: python3 {sys.argv[0]} \"<list1>\" \"<list2>\"",
            file=sys.stderr,
        )
        print(f"Example: python3 {sys.argv[0]} \"1,2,3,4\" \"3,4,5,6\"", file=sys.stderr)
        raise SystemExit(1)

    result = set_operations(first, second)
    show_result(result, first, second)


if __name__ == "__main__":
    main()
