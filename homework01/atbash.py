def encrypt_atbash(plaintext):
    ciphertext = ""
    if len(plaintext) == 0:
        return ""
    for symbol in plaintext:
        if symbol.isupper():
            ciphertext += chr(64 + (26 - (ord(symbol) - 64) + 1))
            # чтобы подставить формулу из условия вычитаем 1, чтобы учесть что нумерация начинается с 1
        elif symbol.islower():
            ciphertext += chr(96 + (26 - (ord(symbol) - 96) + 1))
        else:
            ciphertext += symbol
    return ciphertext


def decrypt_atbash(ciphertext):
    plaintext = ""
    if len(ciphertext) == 0:
        return ""
    for symbol in ciphertext:
        if symbol.isupper():
            plaintext += chr(64 + (26 - (ord(symbol) - 64) + 1) % 26)
        elif symbol.islower():
            plaintext += chr(96 + (26 - (ord(symbol) - 96) + 1) % 26)
        else:
            plaintext += symbol
    return plaintext
