import string
from string import ascii_lowercase

def ceasarCipher(plaintext, shift):
    """ Simple Ceasar cipher used to illustrate key encryption. """
    alphabet = string.ascii_lowercase

    shifted_alphabet = alphabet[shift:] + alphabet[:shift]

    table = string.maketrans(alphabet, shifted_alphabet)

    return plaintext.translate(table)


if __name__ == '__main__':
    main()