from random import choice
from string import digits, ascii_letters


def generate_slug():
    char_set = digits + ascii_letters
    return ''.join(choice(char_set) for _ in range(5))
