from itertools import cycle

def repeating_xor(data, key):
    key = cycle(key)
    encoded = bytearray()
    for byte in data:
        encoded.append(byte ^ next(key))
    return bytes(encoded)

def main():
    key = b'ICE'
    data = ''
    with open('plain') as f:
        data = f.read().encode()

    encoded_data = repeating_xor(data, key)
    print(encoded_data.hex())

if __name__ == '__main__':
    main()
