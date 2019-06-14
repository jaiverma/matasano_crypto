from Crypto.Cipher import AES
import base64

def main():
    key = b'YELLOW SUBMARINE'
    cipher = AES.new(key, AES.MODE_ECB)

    ciphertext = b''
    with open('7.txt') as f:
        ciphertext = f.read().encode()
    ciphertext = base64.b64decode(ciphertext)

    plaintext = cipher.decrypt(ciphertext)
    print(plaintext.decode())

if __name__ == '__main__':
    main()
