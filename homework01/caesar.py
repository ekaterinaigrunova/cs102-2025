"""
Это шифр Цезаря
"""
def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    if len(plaintext) == 0:
        return ""
    for symbol in plaintext:
        if symbol.isupper():
            ciphertext += chr(65 + (ord(symbol) - 65 + shift) % 26)
        elif symbol.islower():
            ciphertext += chr(97 + (ord(symbol) - 97 + shift) % 26)
        else:
            ciphertext += symbol
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    """

    plaintext = ""
    if len(ciphertext) == 0:
        return
    for symbol in ciphertext:
        if symbol.isupper():
            plaintext += chr(65 + (ord(symbol) - 65 - shift) % 26)
        elif symbol.islower():
            plaintext += chr(97 + (ord(symbol) - 97 - shift) % 26)
        else:
            plaintext += symbol

    return plaintext
