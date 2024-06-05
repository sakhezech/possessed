import itertools

import enchant

LETTERS = [i for i in range(97, 97 + 26)]
spellcheck = enchant.Dict('en_US')


def decipher(word: str):
    unknown = {letter for letter in word if letter.islower()}

    products = itertools.product(LETTERS, repeat=len(unknown))
    for product in products:
        translate_table = str.maketrans(
            {
                unknown_letter: possible_letter
                for unknown_letter, possible_letter in zip(unknown, product)
            }
        )
        result = word.translate(translate_table).lower()
        if spellcheck.check(result):
            yield result


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
        for possible_word in decipher(word):
            output.write(possible_word)
            output.write('\n')
    finally:
        output.close()
