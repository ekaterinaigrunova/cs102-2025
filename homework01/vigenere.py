"""
Это шифр Виженера
"""
def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    len_plaintext = len(plaintext)
    len_keyword = len(keyword)
    keyword = keyword.upper()
    if len(plaintext) == 0:
        return ""
    if len_plaintext != len_keyword:
        keyword = (len_plaintext // len_keyword) * keyword + keyword[: len_plaintext % len_keyword]

    for i in range(len_plaintext):
        symbol = plaintext[i]
        shift = ord(keyword[i]) - 65
        if symbol.isupper():
            ciphertext += chr(65 + (ord(symbol) - 65 + shift) % 26)
        elif symbol.islower():
            ciphertext += chr(97 + (ord(symbol) - 97 + shift) % 26)
        else:
            ciphertext += symbol
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    len_ciphertext = len(ciphertext)
    len_keyword = len(keyword)
    keyword = keyword.upper()
    if len(ciphertext) == 0:
        return ""
    if len_ciphertext != len_keyword:
        keyword = ((len_ciphertext // len_keyword) * keyword +
                  keyword[: len_ciphertext % len_keyword])

    for i in range(len_ciphertext):
        symbol = ciphertext[i]
        shift = ord(keyword[i]) - 65
        if symbol.isupper():
            plaintext += chr(65 + (ord(symbol) - 65 - shift) % 26)
        elif symbol.islower():
            plaintext += chr(97 + (ord(symbol) - 97 - shift) % 26)
        else:
            plaintext += symbol

    return plaintext
