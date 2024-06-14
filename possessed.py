import itertools
import re
from typing import Generator, Iterable

import spellchecker

LETTERS = {chr(i) for i in range(97, 97 + 26)}
spellcheck = spellchecker.SpellChecker()
brackets = re.compile(r'\[(\w*?)\]')


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
        if not spellcheck.unknown(spellcheck.split_words(possible_word)):
            yield possible_word


def decipher_with_charsets(
    word: str, letters: set[str]
) -> Generator[str, None, None]:
    charsets: list[list[str]] = [list(set_) for set_ in brackets.findall(word)]
    template = brackets.sub('{}', word)
    charset_combinations = itertools.product(*charsets)
    for charset_combination in charset_combinations:
        new_word = template.format(*charset_combination)
        yield from decipher(new_word, letters)


if __name__ == '__main__':
    import argparse
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description='deciphering tool for the language of the newly announced'
        ' Heart Machine game',
    )
    parser.add_argument(
        '-k',
        '--known',
        default='',
        help='letters which symbols are already known',
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
    letters = LETTERS.copy().difference(set(args.known))

    try:
        for possible_translations in decipher_with_charsets(word, letters):
            output.write(possible_translations)
            output.write('\n')
    finally:
        output.close()
