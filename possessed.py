import itertools
from typing import Iterable

import spellchecker

LETTERS = [chr(i) for i in range(97, 97 + 26)]
spellcheck = spellchecker.SpellChecker()


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


def decipher(word: str) -> set[str]:
    unknown = {letter for letter in word if letter.islower()}
    letter_permutations = itertools.permutations(LETTERS, r=len(unknown))
    possible_words = (
        make_possible_word(word, unknown, permutation)
        for permutation in letter_permutations
    )
    return spellcheck.known(possible_words)


if __name__ == '__main__':
    import argparse
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description='deciphering tool for the language of the newly announced'
        ' Heart Machine game',
    )
    parser.add_argument(
        'cipher',
        help='cipher to decode',
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

    try:
        for possible_translations in decipher(word):
            output.write(possible_translations)
            output.write('\n')
    finally:
        output.close()
