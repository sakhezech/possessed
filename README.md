# POSSESSED

Deciphering tool for the language of the newly announced Heart Machine game.

## Preparations

For this to work you will need:

- `python` - general purpose programming language
- `pyspellchecker` - pure python spell checking

Make a virtual environment and install `pyspellchecker`.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install pyspellchecker
```

## How to use

`python3 possessed.py ...`

Write the letters you know in uppercase and substitute letters you don't know
with some lowercase letters.

For example:

![Cipher](/.github/possessors.png)

If we know that the 1st letter is `P` and 3rd, 4th, 6th, 7th, and 10th letters
are `S` we should invoke the script like this

```sh
python3 possessed.py PaSSbSSacS
```

i.e. we substitute same symbols with same lowercase letters.

For more options see `python3 possessed.py --help`.
