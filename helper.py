import random, string

def simpleCipher(msg, shift, key):
    """ 
        Simple ceasar cipher that scrambles/unscrambles a msg.
        @msg = Message to encrypt.
        @shift = How many characters to shift. integer.
        @key = 'e' (any character) for Encrypt or 'd' for decrypt.
    """
    if key == 'd':
        key = -shift
    else:
        key = shift

    translated = ''

    for symbol in msg:
        if symbol.isalpha():
            num = ord(symbol)
            num += key

            if symbol.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif symbol.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26
            
            translated += chr(num)
        else:
            translated += symbol
    
    return translated
        

def readCert(cert,shift):
    """ Check server certificate. If valid, return true. If not return false """
    
    server_cert = "CA: I am Simple Server Certificate"

    decipher_cert = ceasarCipher(cert, -shift)
    
    result = False
    print("Server cert: ", server_cert, " Decipher Cert: ", decipher_cert)
    if server_cert == decipher_cert:
        result = True
    else:
        result = False

    return result

def randomString(length):
    """ Generate a random string with set length
        @length = Length or string returned.
    """
    alphabet = string.ascii_letters
    return ''.join( random.choice(alphabet) for i in range(length) )

def main():
    """ Test the helper functions """

    print("*************** TEST simpleCipher() ***************")
    certificate = "CA: I am Simple Server Certificate~Server Public Key"
    cert_array = certificate.split("~")
    server_cert = cert_array[0]
    server_public_key = cert_array[1]
    
    print( "Cert: = " + server_cert )
    print("Encrypted = " + simpleCipher(server_cert,1,'e') )
    print( "Decrypted = " + simpleCipher( simpleCipher(server_cert,1,'e') ,1,'d') )

    print("*************** TEST Secret Decipher ***************")
    secret = "Tfswfs Qvcmjd Lfz~Uijt jt Dmjfou Tfdsfu"
    secret_array = certificate.split("~")
    server_key = cert_array[0]
    client_secret = cert_array[1]

    print( "Secret: = " + secret )
    print( "Key Decrypted = " + simpleCipher(server_key,1,'d') )
    print( "Secret Decrypted = " + simpleCipher(client_secret,1,'d') )
    print( "Key+Secret Decrypted = " + simpleCipher( secret,1,'d') )

    print("*************** TEST Random String Generator ***************")
    print( randomString(5) )
    print( randomString(5) )
    print( randomString(6) )
    print( randomString(6) )
    print( randomString(7) )
    print( randomString(7) )

if __name__ == '__main__':
    main()