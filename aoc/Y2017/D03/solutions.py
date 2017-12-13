from ...classes import Solution


def calculate_moves(n):
    """
    This was sadly copy/pasted from StackOverflow.
    """
    #(di, dj) is a vector - direction in which we move right now
    di = 1
    dj = 0
    # length of current segment
    segment_length = 1
    # current position (i, j) and how much of current segment we passed
    i = 0
    j = 0
    segment_passed = 0
    for k in range(n):
        # make a step, add 'direction' vector (di, dj) to current position (i, j)
        i += di
        j += dj
        segment_passed += 1
        yield(i, j)

        if segment_passed == segment_length:
            # one with current segment
            segment_passed = 0

            # 'rotate' directions
            buffer = di
            di = -dj
            dj = buffer

            # increase segment length if necessary
            if dj == 0:
                segment_length += 1


def get_pos(n):
    moves = list(calculate_moves(n))
    return moves[-1]


def nmoves(n):
    x, y = get_pos(n-1)
    return abs(x) + abs(y)


def parse_input(data):
    return int(data[0].strip())


def phase1(data):
    return nmoves(data)


def phase2():
    ...


solution = Solution(2017, 3, phase1=phase1, input_parser=parse_input)
