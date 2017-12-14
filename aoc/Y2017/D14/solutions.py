from ...classes import Solution
from ..functions import knot_hash_string
from ..classes import Graph

def bit_count(value):
    """
    Found on https://wiki.python.org/moin/BitManipulation
    """
    count = 0
    while value:
        count += (value & 1)
        value >>= 1
    return count


def count_used(row):
    return sum(bit_count(val) for val in row)


def values_to_bits(value):
    return [bool(int(c)) for c in bin(value)[2:].zfill(4)]


def row_to_bit_row(row):
    bit_row = []
    for val in row:
        bit_row.extend(values_to_bits(val))
    return bit_row


def build_bit_table(table):
    return [row_to_bit_row(row) for row in table]


def build_table(key):
    table = []
    for row_num in range(128):
        k_hash = knot_hash_string(f'{key}-{row_num}')
        table.append([int(c, 16) for c in k_hash])
    return table


def get_edges(bit_table):
    edges = {}
    for row_idx, row in enumerate(bit_table):
        for col_idx, val in enumerate(row):
            cell_id = (row_idx, col_idx)
            if val:
                edges[cell_id] = []
                for other_row in (row_idx-1, row_idx+1):
                    if is_used(bit_table, other_row, col_idx):
                        edges[cell_id].append((other_row, col_idx))
                for other_col in (col_idx-1, col_idx+1):
                    if is_used(bit_table, row_idx, other_col):
                        edges[cell_id].append((row_idx, other_col))
    return edges


def is_used(bit_table, row, col):
    try:
        if row >= 0 and col >= 0:
            return bit_table[row][col]
    except IndexError:
        pass
    return False


def parse_input(data):
    return data[0].strip()


def phase1(data):
    total_used = 0
    table = build_table(data)
    for row in table:
        total_used += count_used(row)
    return total_used


def phase2(data):
    table = build_table(data)
    bit_table = build_bit_table(table)
    edges = get_edges(bit_table)
    graph = Graph(edges)
    groups = graph.connected_components()
    return len(groups)


solution = Solution(2017, 14, phase1=phase1, phase2=phase2, input_parser=parse_input)

