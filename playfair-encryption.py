import string

def prepare_plaintext(text, filler):
    text = text.lower().replace('j', 'i')
    text = ''.join(c for c in text if c.isalpha())
    
    prepared = ''
    i = 0
    while i < len(text):
        prepared += text[i]
        if i + 1 < len(text) and text[i] == text[i + 1]:
            prepared += filler
        i += 1
    
    if len(prepared) % 2 != 0:
        prepared += filler
    
    return prepared

def playfair(keyword):
    grid = [[], [], [], [], []]
    gridindex = 0
    seen = set()

    for char in keyword.lower().replace('j', 'i'):
        if char in seen:
            continue
        seen.add(char)
        grid[gridindex].append(char)
        if len(grid[gridindex]) % 5 == 0:
            gridindex += 1

    alphabet = [c for c in string.ascii_lowercase if c != 'j' and c not in seen]

    for char in alphabet:
        grid[gridindex].append(char)
        if len(grid[gridindex]) % 5 == 0:
            gridindex += 1

    return grid

def lookup(grid):
    lkp = {}
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            lkp[char] = (r, c)
    return lkp

def playfair_pair(letter1, letter2, grid, lkp):
    r1, c1 = lkp[letter1]
    r2, c2 = lkp[letter2]
    if r1 == r2:
        return grid[r1][(c1 + 1) % 5], grid[r2][(c2 + 1) % 5]
    elif c1 == c2:
        return grid[(r1 + 1) % 5][c1], grid[(r2 + 1) % 5][c2]
    else:
        return grid[r1][c2], grid[r2][c1]

def playfair_pair_decrypt(letter1, letter2, grid, lkp):
    r1, c1 = lkp[letter1]
    r2, c2 = lkp[letter2]
    if r1 == r2:
        return grid[r1][(c1 - 1) % 5], grid[r2][(c2 - 1) % 5]
    elif c1 == c2:
        return grid[(r1 - 1) % 5][c1], grid[(r2 - 1) % 5][c2]
    else:
        return grid[r1][c2], grid[r2][c1]

def playfair_encrypt(plaintext, keyword, filler):
    grid = playfair(keyword)
    lkp = lookup(grid)
    plaintext = prepare_plaintext(plaintext, filler)
    pairs = [(plaintext[i], plaintext[i + 1]) for i in range(0, len(plaintext), 2)]
    return ''.join(c for pair in pairs for c in playfair_pair(*pair, grid, lkp))

def playfair_decrypt(ciphertext, keyword, filler):
    grid = playfair(keyword)
    lkp = lookup(grid)
    ciphertext = ciphertext.lower().replace('j', 'i')
    ciphertext = ''.join(c for c in ciphertext if c.isalpha())
    pairs = [(ciphertext[i], ciphertext[i + 1]) for i in range(0, len(ciphertext), 2)]
    return ''.join(c for pair in pairs for c in playfair_pair_decrypt(*pair, grid, lkp))

encryption_item = input("Enter what you want to be encrypted: ")
keyphrase = input("What is the keyphrase for the cipher? ")
filler_item = input("Please enter the agreed filler in the cipher? ")
encrypted_final = playfair_encrypt(encryption_item, keyphrase, filler_item)
decrypted_final = playfair_decrypt(encrypted_final, keyphrase, filler_item)
print(f'Encrypted: {encrypted_final}')
print(f'Decrypted: {decrypted_final}')
