import string
from string import ascii_lowercase

def ceasarCipher(plaintext, shift):
    """ Simple Ceasar cipher used to illustrate key encryption. """
    alphabet = string.ascii_lowercase

    shifted_alphabet = alphabet[shift:] + alphabet[:shift]

    table = string.maketrans(alphabet, shifted_alphabet)

    return plaintext.translate(table)

def readCert(cert,shift):
    """ Check server certificate. If valid, return true. If not return false """
    
    server_cert = "I am Simple Server"

    decipher_cert = ceasarCipher(cert, -shift)
    
    result = False
    print("Server cert: ", server_cert, " Decipher Cert: ", decipher_cert)
    if server_cert == decipher_cert:
        result = True
    else:
        result = False

    return result


def main():
    """ Test the helper functions """
    server_cert = "I am Simple Server"
    shift = 1
    encoded_cert = ceasarCipher(server_cert,shift)
    print(readCert(encoded_cert,shift))

    print("Encoded Cert: ", ceasarCipher(server_cert,shift))
    print("Dencoded Cert: ", ceasarCipher(encoded_cert,shift))

if __name__ == '__main__':
    main()