import ofb_utils
from sys import platform
import time
import os

def Main():
# File and script path for windows platform
    if platform == "win64" or platform == "win32":
        script_dir = os.path.dirname(__file__) # get script execution path
        plainTextFile = f'{script_dir}\\resources\\plaintext.txt' # plaintext file path
        cipherTextFile = f'{script_dir}\\resources\\ciphertext.txt' # ciphertext file path
        ivFile = f'{script_dir}\\resources\\iv.txt' # iv path

# File and script path for GNU/Linux palatform
    if platform == "linux" or platform == "linux2":
        script_dir = os.getcwd() # get script execution path
        plainTextFile = f'{script_dir}/resources/plaintext.txt' # plaintext file path
        cipherTextFile = f'{script_dir}/resources/ciphertext.txt' # ciphertext file path
        ivFile = f'{script_dir}/resources/iv.txt' # iv path

#### input key ####
    keyString = input("\nPlease Enter your key: ")
    while(len(keyString) != 16):
        print("Lenght of the key should be 16. try again:", end='')
        keyString = input()

#### encryption ####
    print('\nbegining encryption:')
    origIV = ofb_utils.ofb_encrypt(plainTextFile, keyString, cipherTextFile) # encrypt plaintext.txt and save it as ciphertext.txt
    ofb_utils.writeIV(origIV, ivFile) # write iv to file
    
#### decryption ####
    origIV = ofb_utils.readIV(ivFile) # read iv from file
    print('\nbegining decryption:')
    ofb_utils.ofb_decrypt(cipherTextFile, keyString, origIV, plainTextFile) # decrypt ciphertext.txt networksecurity0and save it as plaintext.txt




if __name__ == "__main__":
    stime = time.time()
    Main()
    print("\nscript execution time: {0}\n".format(time.time() - stime) )