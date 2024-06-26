import itertools
import re
from typing import Generator, Iterable

import spellchecker

SPELLCHECKER = spellchecker.SpellChecker()
BRACKET_REGEX = re.compile(r'\[(\w*?)\]')


def make_possible_word(
    word: str,
    unknown: Iterable[str],
    permutation: Iterable[str],
) -> str:
    translate_table = str.maketrans(
        {
            unknown_letter: possible_letter
            for unknown_letter, possible_letter in zip(unknown, permutation)
        }
    )
    return word.translate(translate_table).lower()


def decipher(word: str, letters: set[str]) -> Generator[str, None, None]:
    unknown = {letter for letter in word if letter.islower()}
    letter_permutations = itertools.permutations(letters, r=len(unknown))
    possible_words = (
        make_possible_word(word, unknown, permutation)
        for permutation in letter_permutations
    )
    for possible_word in possible_words:
        if not SPELLCHECKER.unknown(SPELLCHECKER.split_words(possible_word)):
            yield possible_word


def decipher_with_charsets(
    word: str, letters: set[str]
) -> Generator[str, None, None]:
    charsets: list[list[str]] = [
        list(set_) for set_ in BRACKET_REGEX.findall(word)
    ]
    template = BRACKET_REGEX.sub('{}', word)
    charset_combinations = itertools.product(*charsets)
    for charset_combination in charset_combinations:
        new_word = template.format(*charset_combination)
        yield from decipher(new_word, letters)


if __name__ == '__main__':
    import argparse
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description="""
        deciphering tool for the language of Possessor(s), Heart Machine's new
        announced game
        """,
    )
    parser.add_argument(
        '-k',
        '--known',
        default='',
        help='letters which symbols are already known',
    )
    parser.add_argument(
        'cipher',
        help="""
        cipher, known letters in uppercase and substitute unknown
        symbols with lowercase letters, put multiple letters in
        brackets like '[DC]ash' for 'Dash' and 'Cash'
        """,
    )
    parser.add_argument(
        '-o',
        '--output',
        type=Path,
        help='output file (defaults to stdout)',
    )
    args = parser.parse_args()

    word: str = args.cipher if args.cipher != '-' else sys.stdin.read()
    output = args.output.open('w') if args.output is not None else sys.stdout

    all_letters = {chr(i) for i in range(97, 97 + 26)}
    letters = all_letters.difference(set(args.known))

    try:
        for possible_translation in decipher_with_charsets(word, letters):
            output.write(possible_translation)
            output.write('\n')
    finally:
        output.close()
