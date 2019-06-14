def detect_ecb(ciphertext):
    blocks = []
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i + 16]
        blocks.append(block)

    unique_blocks = set(blocks)
    if len(unique_blocks) != len(blocks):
        block_count = {block : blocks.count(block) for block in unique_blocks}
        return True, block_count
    return False, {block : 1 for block in blocks}


def main():
    data = b''
    with open('8.txt') as f:
        for line in f:
            ciphertext = bytes.fromhex(line.strip())
            is_ecb, block_count = detect_ecb(ciphertext)
            if is_ecb:
                print('Ciphertext encrypted with AES-ECB: {}'.format(ciphertext))
                print(block_count)

if __name__ == '__main__':
    main()
