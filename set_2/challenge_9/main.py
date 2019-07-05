def pkcs7(data, block_size):
    padding_len = block_size - len(data)
    padding = bytes([padding_len]) * padding_len
    return data + padding

def main():
    data = b'YELLOW SUBMARINE'
    print(pkcs7(data, 20))

if __name__ == '__main__':
    main()
