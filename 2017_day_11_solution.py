from utils import get_input
import collections


def calculate_goal_coordinates(path):
    start = Hex(0, 0, 0)
    current = start
    for step in path:
        current = Hex.hex_neigbor(current, step)
    return current


def path_to_directions(path):
    out = []
    for idx, pos in enumerate(path):
        if idx+1 < len(path):
            dir_num = Hex.hex_subtract(path[idx+1],pos)
            for name, val in HEX_DIRECTIONS.items():
                if val == dir_num:
                    out.append(name)
        else:
            return out


class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()


class Graph:
    def __init__(self):
        self.edges = {}
        self.came_from = {}

    def neighbors(self, id):
        if id not in self.edges:
            self.edges[id] = [Hex.hex_neigbor(id, direction) for direction in HEX_DIRECTIONS.keys()]
        return self.edges[id]

    def breadth_first_search(self, start, goal):
        frontier = Queue()
        frontier.put(start)
        self.came_from = {}
        self.came_from[start] = None

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in self.neighbors(current):
                if next not in self.came_from:
                    frontier.put(next)
                    self.came_from[next] = current

        return self.came_from

    def get_path(self, node):
        out = [node]
        current = node
        while current != Hex(0, 0, 0):
            current = self.came_from[current]
            out.append(current)
        out.reverse()
        return out


class Hex:

    def __init__(self, q, r, s):
        self.q = q
        self.r = r
        self.s = s

    def __eq__ (self, other):
        if (self.q == other.q) and (self.r == other.r) and (self.s == other.s):
            return True
        return False

    @staticmethod
    def hex_add(a, b):
        return Hex(a.q + b.q, a.r + b.r, a.s + b.s)

    @staticmethod
    def hex_subtract(a, b):
        return Hex(a.q - b.q, a.r - b.r, a.s - b.s)

    @staticmethod
    def hex_length(h):
        return int((abs(h.q) + abs(h.r) + abs(h.s)) / 2)

    @staticmethod
    def hex_distance(a, b):
        return Hex.hex_length(Hex.hex_subtract(a, b))

    @staticmethod
    def hex_neigbor(h, direction):
        return Hex.hex_add(h, HEX_DIRECTIONS[direction])

    def __hash__(self):
        return hash((self.q, self.r, self.s))

    def __repr__(self):
        return f'q: {self.q}, r: {self.r}, s: {self.s}'


HEX_DIRECTIONS = {
        'SE': Hex(1, 0, -1), 'NE': Hex(1, -1, 0), 'N':Hex(0, -1, 1),
        'NW': Hex(-1, 0, 1), 'SW': Hex(-1, 1, 0), 'S':Hex(0, 1, -1)
    }


def path_from_origin(destination):
    g = Graph()
    g.breadth_first_search(Hex(0,0,0), destination)
    path = g.get_path(destination)
    steps = path_to_directions(path)
    return steps


def parse_input(input):
    return [i.strip().upper() for i in input[0].split(',')]


def solution_11_1(input):
    goal = calculate_goal_coordinates(input)
    return Hex.hex_distance(Hex(0, 0, 0), goal)


def solution_11_2(input):
    distances = []
    for idx in range(len(input)):
        pos = calculate_goal_coordinates(input[:len(input)-idx])
        distances.append(Hex.hex_distance(Hex(0, 0, 0), pos))
    return max(distances)


if __name__ == '__main__':
    print(solution_11_1(parse_input(get_input(2017, 11))))
    print(solution_11_2(parse_input(get_input(2017, 11))))