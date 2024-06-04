# POSSESSED

Deciphering tool for the language of the newly announced Heart Machine game.

## Preparations

For this to work you will need:

- `python` - general purpose programming language
- `enchant` - wrapper library for generic spell checking
- `pyenchant` - python bindings for `enchant`
- `nuspell` - spellchecking C++ library
- `hunspell-en_us` - US English dictionary

```sh
# for Arch
sudo pacman -S enchant nuspell hunspell-en_us
# for Ubuntu
sudo apt install enchant-2 nuspell hunspell-en-us python3-venv
```

Make a virtual environment and install `pyenchant`.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install pyenchant
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
