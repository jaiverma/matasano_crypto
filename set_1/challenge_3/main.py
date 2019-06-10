def score(data):
    # Frequencies taken from http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
    score_table = {
        'E': 12.02,
        'T': 9.10,
        'A': 8.12,
        'O': 7.68,
        'I': 7.31,
        'N': 6.95,
        'S': 6.28,
        'R': 6.02,
        'H': 5.92,
        'D': 4.32,
        'L': 3.98,
        'U': 2.88,
        'C': 2.71,
        'M': 2.61,
        'F': 2.30,
        'Y': 2.11,
        'W': 2.09,
        'G': 2.03,
        'P': 1.82,
        'B': 1.49,
        'V': 1.11,
        'K': 0.69,
        'X': 0.17,
        'Q': 0.11,
        'J': 0.10,
        'Z': 0.07
    }
    return sum(score_table.get(i, 0) for i in data.upper())

def xor(s, key):
    ans = bytearray()
    for i in s:
        ans.append(i ^ key)
    return bytes(ans)

def main():
    s = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    s = bytes.fromhex(s)
    scores = []

    for key in range(256):
        decoded_s = xor(s, key)
        try:
            decoded_s = decoded_s.decode('utf-8')
        except UnicodeDecodeError:
            pass
        else:
            scores.append({
                'score': score(decoded_s),
                'data': decoded_s
            })

    scores = sorted(scores, key=lambda x: x['score'], reverse=True)
    for i in scores[:10]:
        print(i['data'])

if __name__ == '__main__':
    main()

# Cooking MC's like a pound of bacon
