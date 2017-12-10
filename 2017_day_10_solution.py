from utils import get_input
from collections import namedtuple


def hash1(lenghts):
    current_position = 0
    skip_size = 0
    l = list(range(256))
    for length in lenghts:
        length = int(length)
        if length > 0:
            start_idx = current_position % 256
            end_idx = ((current_position + length) % 256)
            if end_idx > start_idx:
                digits = l[start_idx:end_idx]
            else:
                digits = l[start_idx:]
                for d in l[:end_idx]:
                    digits.append(d)
            while len(digits) > 0:
                l[current_position%256] = digits.pop()
                current_position = (current_position+1)%256
        current_position += skip_size
        skip_size += 1
    return l


def decode_input(lenghts):
    decoded_lenghts = []
    for encoded_length in lenghts:
        decoded_lenghts.extend(ord(c) for c in encoded_length)
    decoded_lenghts.extend([17, 31, 73, 47, 23])
    return decoded_lenghts


def hash2(lenghts, l, current_position, skip_size):
    for length in lenghts:
        if length > 0:
            start_idx = current_position % 256
            end_idx = ((current_position + length) % 256)
            if end_idx > start_idx:
                digits = l[start_idx:end_idx]
            else:
                digits = l[start_idx:]
                for d in l[:end_idx]:
                    digits.append(d)
            while len(digits) > 0:
                l[current_position%256] = digits.pop()
                current_position = (current_position+1)%256
        current_position += skip_size
        skip_size += 1
    return l, current_position, skip_size


def parse_input(input):
    return [i.strip() for i in input[0].split(',')]


def solution_10_1(input):
    hashed = hash1(input)
    return hashed[0] * hashed[1]


def solution_10_2(input):
    input_string = ','.join(input)
    lenghts = decode_input(input_string)
    current_position = skip_size = 0
    l = list(range(256))
    for _ in range(64):
        l, current_position, skip_size = hash2(lenghts, l, current_position, skip_size)
    dense = []
    for pos in range(16):
        block = l[16*pos:(16*pos)+16]
        dense_block = block[0]
        for byte in block[1:]:
            dense_block = dense_block ^ byte
        dense.append(dense_block)
    return ''.join(f'{d:2x}' for d in dense).replace(' ', '0')

if __name__ == '__main__':
    print(solution_10_1(parse_input(get_input(2017, 10))))
    print(solution_10_2(parse_input(get_input(2017, 10))))