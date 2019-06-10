import base64

def b64(s):
    s = bytes.fromhex(s)
    return base64.b64encode(s)

def main():
    s = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    print(b64(s))

if __name__ == '__main__':
    main()
