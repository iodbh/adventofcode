def knot_hash_round(values, l=None, current_position=0, skip_size=0):
    if l is None:
        l = list(range(256))
    for length in values:
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


def knot_hash_string(string, rounds=64):
    suffix = (17, 31, 73, 47, 23)
    values = [ord(c) for c in string]
    current_position = skip_size = 0
    values.extend(suffix)
    l = list(range(256))
    for _ in range(rounds):
        l, current_position, skip_size = knot_hash_round(values, l, current_position, skip_size)
    dense = []
    for pos in range(16):
        block = l[16 * pos:(16 * pos) + 16]
        dense_block = block[0]
        for byte in block[1:]:
            dense_block = dense_block ^ byte
        dense.append(dense_block)
    return ''.join(f'{d:02x}' for d in dense)