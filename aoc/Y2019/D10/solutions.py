from ...classes import Solution
from collections import namedtuple
from itertools import combinations

Point = namedtuple("Point", "x y")


class AsteroidsMap:

    GRID_SCALE_FACTOR = 21
    GRID_SCALE_OFFSET = (GRID_SCALE_FACTOR - 1) // 2

    def __init__(self, data):

        self.data = data

        self.asteroids = {}
        self.height = len(data)
        self.width = len(data[0])

        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                if cell == "#":
                    self.asteroids[Point(x, y)] = set()

    def calculate_lines_of_sight(self):
        for asteroid_1, asteroid_2 in combinations(self.asteroids, 2):
            # using bresenham implementation from :
            # https://github.com/encukou/bresenham/blob/master/bresenham.py
            if asteroid_2 in self.asteroids[asteroid_1]:
                continue
            line_of_sight = True

            dx = asteroid_2.x - asteroid_1.x
            dy = asteroid_2.y - asteroid_1.y

            xsign = 1 if dx > 0 else -1
            ysign = 1 if dy > 0 else -1

            dx = abs(dx)
            dy = abs(dy)

            if dx > dy:
                xx, xy, yx, yy = xsign, 0, 0, ysign
            else:
                dx, dy = dy, dx
                xx, xy, yx, yy = 0, ysign, xsign, 0

            D = 2 * dy - dx
            y = 0

            for x in range(dx + 1):
                current_x = asteroid_1.x + x * xx + y * yx
                current_y = asteroid_1.y + x * xy + y * yy

                # check for blocking asteroid
                current = Point(current_x, current_y)
                if current not in (asteroid_1, asteroid_2) and current in self.asteroids:
                    self.asteroids[asteroid_1].add(current)
                    self.asteroids[current].add(asteroid_1)
                    line_of_sight = False
                    break
                if D >= 0:
                    y += 1
                    D -= 2 * dx
                D += 2 * dy
            if line_of_sight:
                self.asteroids[asteroid_1].add(asteroid_2)
                self.asteroids[asteroid_2].add(asteroid_1)

    def scale_point(self, point, action):
        if action == "+":
            x = point.x * self.GRID_SCALE_FACTOR + self.GRID_SCALE_OFFSET
            y = point.y * self.GRID_SCALE_FACTOR + self.GRID_SCALE_OFFSET
        elif action == "-":
            x = (point.x - self.GRID_SCALE_OFFSET) // self.GRID_SCALE_FACTOR
            y = (point.y - self.GRID_SCALE_OFFSET) // self.GRID_SCALE_FACTOR
        else:
            raise ValueError('action argument must be "+" or "-"')
        return Point(x=x, y=y)

    def scale_grid(self, action):
        new_grid = {}
        for asteroid, los in self.asteroids.items():
            new_key = self.scale_point(asteroid, action)
            new_val = {self.scale_point(p, action) for p in los}
            new_grid[new_key] = new_val
        self.asteroids = new_grid


def parse_input(data):

    return [line.strip() for line in data]


def phase1(data):
    starmap = AsteroidsMap(data)
    starmap.scale_grid("+")
    starmap.calculate_lines_of_sight()
    starmap.scale_grid("-")
    max_los = 0
    for asteroid, los in starmap.asteroids.items():
        if len(los) > max_los:
            max_los = len(los)

    return max_los


def phase2(data):
    return None


solution = Solution(2019, 10, phase1=phase1, input_parser=parse_input, test=False)
