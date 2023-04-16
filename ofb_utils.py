from des import DesKey
from random import randbytes
import copy

#### utils ####
def split_str(s, w):
    return [s[i:i + w] for i in range(0, len(s), w)]


#### IO ####
def readPlainText(path):
    with open(path, 'r', encoding='utf8') as file:
        result = file.read()
        return result

def writePlainText(plainText, path):
    with open(path, 'w', encoding='utf8') as file:
        file.write(plainText)

def readCipherText(path):
    with open(path, 'rb') as file:
        result = file.read()
        return result

def writeCipherText(cipherText, path):
    with open(path, 'wb') as file:
        file.write(cipherText)

def readIV(path):
    with open(path, 'rb') as file:
        result = file.read()
        return result

def writeIV(IV, path):
    with open(path, 'wb') as file:
        file.write(IV)


#### encrypt and decrypt block ####
def ofb_encrypt_block(textChunk, keyBytes, iv):    
    key = DesKey(keyBytes)
    nextIV = key.encrypt(iv)

    textSplitStr = split_str(textChunk,16)
    cipherText = b''

    for i in range(4):
        cipherText += bytes(a ^ b for a, b in zip(nextIV, bytes(textSplitStr[i], 'UTF-8')))
    
    return (nextIV, cipherText) 
    
def ofb_decrypt_block(textChunk, keyBytes, iv):    
    key = DesKey(keyBytes)
    nextIV = key.encrypt(iv)

    textSplitStr = split_str(textChunk,16)
    cipherText = b''

    for i in range(4):
        cipherText += bytes(a ^ b for a, b in zip(nextIV, textSplitStr[i]))
    
    return (nextIV, cipherText) 


#### encrypt and decrypt file ####
def ofb_encrypt(palinTextFile, keyString, cipherTextFile):
    print('plaintext file: ', palinTextFile)
    print('encrypting file: ', end='')
    plainText = readPlainText(palinTextFile)
    plainTextChunks = split_str(plainText, 64)
    if len(plainTextChunks[-1]) < 64:
        while len(plainTextChunks[-1]) != 64:
            plainTextChunks[-1] += '0' 
    
    iv = randbytes(16)
    origIV = copy.deepcopy(iv)
    keyBytes = bytes(keyString,'UTF-8') 

    cipherText = b''
    for Chunck in plainTextChunks:
        iv, cipher = ofb_encrypt_block(Chunck, keyBytes, iv)
        cipherText += cipher
    print('done')

    print('saving file: ', end='')
    writeCipherText(cipherText, cipherTextFile)
    print('done')
    print('ciphertext file: ', cipherTextFile)


    return origIV

def ofb_decrypt(cipherTextFile, keyString, origIV, plainTextFile):
    print('ciphertext file: ', cipherTextFile)
    print('decrypting file: ', end='')
    cipherText = readCipherText(cipherTextFile)
    cipherTextChunks = split_str(cipherText, 64)

    keyBytes = bytes(keyString,'UTF-8')

    plainText = b''
    iv = origIV
    plain = b''
    for Chunck in cipherTextChunks:
        iv, plain = ofb_decrypt_block(Chunck, keyBytes, iv)
        plainText += plain
    print('done')

    res = plainText.decode("utf-8")
    print(f'\nplaintext: {res}\n')

    print('saving file: ', end='')
    writePlainText(res, plainTextFile)
    print('done')
    print('plaintext file: ', plainTextFile)


