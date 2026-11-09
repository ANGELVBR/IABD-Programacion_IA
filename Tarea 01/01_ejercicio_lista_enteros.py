"""Ejercicio: limpiar una lista de enteros.

 Reglas:
 1. Eliminar los números negativos.
 2. Eliminar los repetidos (quedarse con una sola aparición).
 3. Devolver los números ordenados de menor a mayor.
"""
import sys

def cleanList(numeros: list[int]) -> list[int]:
    """Return list of integer without negatives, without repeat  and with order asc."""
    return sorted({numero for numero in numeros if numero >= 0})


def parserNumber(textParam: str) -> list[int]:
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
        numbersInput = parserNumber(", ".join(sys.argv[1:]))
    else:
        print("Write the number with blank space or with , (ej: 3 -1 2 2 7) or (3,-1,2,2,7)")
        numbersInput = parserNumber(input("> "))

    result = cleanList(numbersInput)
    print(f"Input: {numbersInput}")
    print(f"Output : {result}")


if __name__ == "__main__":
    main()
