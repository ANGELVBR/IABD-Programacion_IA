"""Problema 1: Procesamiento de una lista de enteros..

    Crea una función que reciba una lista de enteros por parámetro y devuelva otra lista, de acuerdo a las siguientes acciones:

    1. Eliminar los números negaƟvos de la lista.
    2. Eliminar los valores que están repeƟdos, quedándonos con uno de ellos.
    3. Ordenar los números resultantes de menor a mayor.

Por ejemplo, si le pasara [4, -1, 2, 4, 3, -5, 2], debería retornar [2,3,4].
"""
import sys

def clean_list(numeros: list[int]) -> list[int]:
    """Return list of integer without negatives, without repeat  and with order asc."""
    return sorted({numero for numero in numeros if numero >= 0})


def parser_number(textParam: str) -> list[int]:
    """Convert text type '3 -1 2, 2' to integer list."""
    textParam = textParam.replace(",", " ")
    numberList = []
    for item in textParam.split():
        try:
            numberList.append(int(item))
        except ValueError:
            raise SystemExit(f"Error: '{item}' isn´t integer number.")
    return numberList


def main() -> None:
    if len(sys.argv) > 1:
        numbersInput = parser_number(", ".join(sys.argv[1:]))
    else:
        print("Write the number with blank space or with , (ej: 3 -1 2 2 7) or (3,-1,2,2,7)")
        numbersInput = parser_number(input("> "))

    result = clean_list(numbersInput)
    print(f"Input: {numbersInput}")
    print(f"Output : {result}")


if __name__ == "__main__":
    main()
