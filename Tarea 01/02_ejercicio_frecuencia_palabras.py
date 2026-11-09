#!/usr/bin/env python3
"""Problema 2: Frecuencia de palabras en un texto.

Escribe una función que reciba por parámetro una lista de palabras y la ruta a
un fichero de texto y devuelva un diccionario que muestre cuantas veces
aparecen las disƟntas palabras de la lista en el fichero de texto. Haz un pequeño
programa que la ponga a prueba.
"""

import sys


def normalize_word(word: str) -> str:
    """Lowercase the word and strip punctuation characters from both ends."""
    word = word.lower()
    start, end = 0, len(word)
    while start < end and not word[start].isalnum():
        start += 1
    while end > start and not word[end - 1].isalnum():
        end -= 1
    return word[start:end]


def tokenize(text: str) -> list[str]:
    """Split the text into words: lowercase and no punctuation marks."""
    text = text.lower()
    # Any character that is not a letter, digit or whitespace becomes a space.
    cleaned = "".join(c if c.isalnum() or c.isspace() else " " for c in text)
    return cleaned.split()


def count_words(words: list[str], file_path: str) -> dict[str, int]:
    """Count how many times each word of the list appears in the file.

    Returns a dictionary {word: frequency}. Words that do not appear in the
    text are included with a frequency of 0.
    """
    if not words:
        raise ValueError("The word list cannot be empty.")

    try:
        with open(file_path, encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        raise SystemExit(f"Error: the file '{file_path}' does not exist.")
    except OSError as error:
        raise SystemExit(f"Error reading '{file_path}': {error}")

    searched = {normalize_word(word) for word in words}
    searched.discard("")

    frequencies = {word: 0 for word in searched}
    for token in tokenize(text):
        if token in frequencies:
            frequencies[token] += 1

    return frequencies


def show_result(frequencies: dict[str, int], file_path: str) -> None:
    """Print the words in alphabetical order together with their frequency."""
    print(f"Analyzed file: {file_path}")
    print(f"{'WORD':<20}{'FREQUENCY'}")
    print("-" * 30)
    for word in sorted(frequencies):
        print(f"{word:<20}{frequencies[word]}")
    print("-" * 30)
    print(f"Total distinct words from the list: {len(frequencies)}")

def showAlert() -> None:
    print(
        f"Usage: python3 {sys.argv[0]} <file_path> <word> [<word> ...]",
        file=sys.stderr,
    )
    print(
        f"Example: python3 {sys.argv[0]} sample_text.txt el sol gato",
        file=sys.stderr,
    )

def main() -> None:
    arguments = sys.argv[1:]

    if len(arguments) >= 2:
        file_path = arguments[0]
        words = arguments[1:]
    elif not arguments:
        print("Type the path of the file (e.g. 02_example_text.txt)")
        file_path = input("> ").strip()
        print("Type the list of the wore (e.g. viajero, anciano)")
        words = input("> ").split()
    else:
        print(
            f"Usage: python3 {sys.argv[0]} \"<path_of_file>\" \"<list_of_word>\"",
            file=sys.stderr,
        )
        print(f"Example: python3 {sys.argv[0]} \"02_example_text.txt\" \"viajero, anciano\"", file=sys.stderr)
        raise SystemExit(1)


    frequencies = count_words(words, file_path)
    show_result(frequencies, file_path)


if __name__ == "__main__":
    main()
