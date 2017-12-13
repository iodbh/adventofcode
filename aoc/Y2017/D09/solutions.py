from ...classes import Solution

STATE_INIT = 0
STATE_GROUP = 1
STATE_GARBAGE = 2
STATE_ESCAPE = 3


class StreamParser:

    def __init__(self):
        self.depth = 0
        self.score = 0
        self.garbage_count = 0
        self.state = STATE_INIT
        self.previous_state = {}

    def _switch_state(self, new_state):
        self.previous_state[new_state] = self.state
        self.state = new_state

    def _restore_state(self):
        self.state = self.previous_state[self.state]

    def parse(self, stream):
        for char in stream:
            if self.state == STATE_ESCAPE:
                self._restore_state()
                continue
            elif char == '!':
                self._switch_state(STATE_ESCAPE)
            elif self.state == STATE_GARBAGE:
                if char == '>':
                    self._restore_state()
                    continue
                else:
                    self.garbage_count += 1
            elif self.state in (STATE_INIT, STATE_GROUP):
                if char == '{':
                    self._switch_state(STATE_GROUP)
                    self.depth += 1
                elif char == '}':
                    self._restore_state()
                    self.score += self.depth
                    self.depth -= 1
                elif char == '<':
                    self._switch_state(STATE_GARBAGE)


def parse_input(data):
    return data[0]


def phase1(data):
    parser = StreamParser()
    parser.parse(data)
    return parser.score


def phase2(data):
    parser = StreamParser()
    parser.parse(data)
    return parser.garbage_count


solution = Solution(2017, 9, phase1=phase1, phase2=phase2, input_parser=parse_input)
