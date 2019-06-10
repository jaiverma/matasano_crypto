import base64

def xor(a, b):
    '''
    Takes 2 'bytes' objects and returns xored bytes object
    '''
    assert(len(a) == len(b))
    c = bytearray()
    for i, j in zip(a, b):
        c.append(i ^ j)
    return bytes(c)

def main():
    a = '1c0111001f010100061a024b53535009181c'
    b = '686974207468652062756c6c277320657965'

    a = bytes.fromhex(a)
    b = bytes.fromhex(b)

    c = xor(a, b)

    print(c.hex())

if __name__ == '__main__':
    main()
