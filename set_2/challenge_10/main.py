from Crypto.Cipher import AES
import base64

def pkcs7(data, block_size):
    padding_len = block_size - len(data)
    padding = bytes([padding_len]) * padding_len
    return data + padding

def unpad_pkcs7(data, block_size):
    if len(data) == block_size:
        pad_byte = data[-1]
        if all([True if i == pad_byte else False for i in data[-pad_byte:]]):
            return data[:-pad_byte]
    return data 

def encrypt_block_ecb(cipher, plaintext, iv):
    padded_block = pkcs7(plaintext, 16)
    block = bytes([i ^ j for i, j in zip(padded_block, iv)])
    ciphertext = cipher.encrypt(block)
    return ciphertext

def decrypt_block_ecb(cipher, ciphertext, iv):
    plaintext = cipher.decrypt(ciphertext)
    plaintext = bytes([i ^ j for i, j in zip(plaintext, iv)])
    return unpad_pkcs7(plaintext, 16)

def cbc_encrypt_with_ecb(key, plaintext, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = b''
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i + 16]
        cipher_block = encrypt_block_ecb(cipher, block, iv)
        iv = cipher_block
        ciphertext += cipher_block
    return ciphertext

def cbc_decrypt_with_ecb(key, ciphertext, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = b''
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i + 16]
        plain_block = decrypt_block_ecb(cipher, block, iv)
        iv = block
        plaintext += plain_block
    return plaintext

def main():
    data = b''
    with open('10.txt') as f:
        data = f.read().encode()
    data = base64.b64decode(data)
    key = b'YELLOW SUBMARINE'
    iv = bytes([0x0 for i in range(16)])
    plaintext = cbc_decrypt_with_ecb(key, data, iv)
    print(plaintext.decode('utf-8'))

if __name__ == '__main__':
    main()
