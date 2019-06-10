import base64
from itertools import cycle

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

def repeating_xor(data, key):
    key = cycle(key)
    encoded = bytearray()
    for byte in data:
        encoded.append(byte ^ next(key))
    return bytes(encoded)

def decode(s):
    scores = []

    for key in range(256):
        decoded = xor(s, key)
        try:
            decoded_s = decoded.decode('utf-8')
        except UnicodeDecodeError:
            pass
        else:
            scores.append({
                'score': score(decoded_s),
                'data': decoded_s,
                'key': key
            })

    scores = sorted(scores, key=lambda x: x['score'], reverse=True)
    scores = scores[:5]
    scores = list(filter(lambda x: all(True if (ord(i) >= 10) and (ord(i) <= 126) else False for i in x['data']), scores))
    return scores

def number_of_bits(data):
    n_bits = 0
    while(data > 0):
        n_bits += data & 1
        data >>= 1
    return n_bits

def hamming_distance(a, b):
    hamming_dist = 0
    for i, j in zip(a, b):
        hamming_dist += number_of_bits(i ^ j)
    return hamming_dist

def find_keysize(data, sample_size):
    scores = []
    for keysize in range(2, 41):
        samples = []
        for sample_i in range(sample_size):
            samples.append(data[sample_i * keysize:sample_i * keysize + keysize])

        hamming_dists = [hamming_distance(samples[i], samples[i+1]) for i in range(sample_size - 1)]
        normalized_hamming_dist = sum(i / keysize for i in hamming_dists) / len(hamming_dists)
        scores.append({
            'keysize': keysize,
            'hamming_distance': normalized_hamming_dist
        })
    return sorted(scores, key=lambda x: x['hamming_distance'])

def transpose_blocks(blocks):
    if len(blocks[-1]) != len(blocks[0]):
        blocks.pop()
    transposed = [bytearray() for i in range(len(blocks[0]))]
    for block in blocks:
        for i in range(len(block)):
            transposed[i].append(block[i])

    return [bytes(i) for i in transposed]

def main():
    data = ''
    with open('6.txt') as f:
        data = f.read().encode()
    data = base64.b64decode(data)
    candidate_keysizes = []
    candidate_keysizes.extend(find_keysize(data, 2)[:5])
    candidate_keysizes.extend(find_keysize(data, 4)[:5])
    candidate_keysizes = set(i['keysize'] for i in candidate_keysizes)

    for keysize in candidate_keysizes:
        pass_count = 0
        pass_scores = []
        blocks = []
        for i in range(0, len(data), keysize):
            blocks.append(data[i:i + keysize])
        transposed_blocks = transpose_blocks(blocks)
        for block in transposed_blocks:
            scores = decode(block)
            if len(scores) > 0:
                pass_count += 1
                pass_scores.append(scores)
        if pass_count == keysize:
            break

    keys = [bytearray() for i in range(len(max(pass_scores, key=lambda x: len(x))))]
    for score in pass_scores:
        cycle_score = cycle(score)
        for i in range(len(keys)):
            keys[i].append(next(cycle_score)['key'])

    key = b'Terminator X: Bring the noise'
    decoded = repeating_xor(data, key)
    print(decoded.decode('utf-8'))

if __name__ == '__main__':
    main()

# key: 'Terminator X: Bring the noise'
# Decoded ciphertext:
# I'm back and I'm ringin' the bell
# A rockin' on the mike while the fly girls yell
# In ecstasy in the back of me
# Well that's my DJ Deshay cuttin' all them Z's
# Hittin' hard and the girlies goin' crazy
# Vanilla's on the mike, man I'm not lazy.

# I'm lettin' my drug kick in
# It controls my mouth and I begin
# To just let it flow, let my concepts go
# My posse's to the side yellin', Go Vanilla Go!

# Smooth 'cause that's the way I will be
# And if you don't give a damn, then
# Why you starin' at me
# So get off 'cause I control the stage
# There's no dissin' allowed
# I'm in my own phase
# The girlies sa y they love me and that is ok
# And I can dance better than any kid n' play

# Stage 2 -- Yea the one ya' wanna listen to
# It's off my head so let the beat play through
# So I can funk it up and make it sound good
# 1-2-3 Yo -- Knock on some wood
# For good luck, I like my rhymes atrocious
# Supercalafragilisticexpialidocious
# I'm an effect and that you can bet
# I can take a fly girl and make her wet.

# I'm like Samson -- Samson to Delilah
# There's no denyin', You can try to hang
# But you'll keep tryin' to get my style
# Over and over, practice makes perfect
# But not if you're a loafer.

# You'll get nowhere, no place, no time, no girls
# Soon -- Oh my God, homebody, you probably eat
# Spaghetti with a spoon! Come on and say it!

# VIP. Vanilla Ice yep, yep, I'm comin' hard like a rhino
# Intoxicating so you stagger like a wino
# So punks stop trying and girl stop cryin'
# Vanilla Ice is sellin' and you people are buyin'
# 'Cause why the freaks are jockin' like Crazy Glue
# Movin' and groovin' trying to sing along
# All through the ghetto groovin' this here song
# Now you're amazed by the VIP posse.

# Steppin' so hard like a German Nazi
# Startled by the bases hittin' ground
# There's no trippin' on mine, I'm just gettin' down
# Sparkamatic, I'm hangin' tight like a fanatic
# You trapped me once and I thought that
# You might have it
# So step down and lend me your ear
# '89 in my time! You, '90 is my year.

# You're weakenin' fast, YO! and I can tell it
# Your body's gettin' hot, so, so I can smell it
# So don't be mad and don't be sad
# 'Cause the lyrics belong to ICE, You can call me Dad
# You're pitchin' a fit, so step back and endure
# Let the witch doctor, Ice, do the dance to cure
# So come up close and don't be square
# You wanna battle me -- Anytime, anywhere

# You thought that I was weak, Boy, you're dead wrong
# So come on, everybody and sing this song

# Say -- Play that funky music Say, go white boy, go white boy go
# play that funky music Go white boy, go white boy, go
# Lay down and boogie and play that funky music till you die.

# Play that funky music Come on, Come on, let me hear
# Play that funky music white boy you say it, say it
# Play that funky music A little louder now
# Play that funky music, white boy Come on, Come on, Come on
# Play that funky music
