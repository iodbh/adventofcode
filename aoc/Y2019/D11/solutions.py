from ...classes import Solution
from ..classes import IntCode
from operator import add
from collections import namedtuple

Point = namedtuple("Point", "x y")

COLORS = {
    0: f'\033[40m  \033[0m',
    1: f'\033[47m  \033[0m',
}


class HullPaintingRobot:

    DIR_COUNTER_CLOCKWISE = 0
    DIR_CLOCKWISE = 1
    COL_BLACK = 0
    COL_WHITE = 1

    def __init__(self, program, start_on_white=False):

        self.brain = IntCode(program, silent=True, input_wait=True)
        self.position = [0, 0]
        self.direction = [0, 1]
        self.painted_positions = {}
        self.start_on_white = start_on_white

    def go(self):
        waiting = True
        inputs = [int(self.start_on_white)]
        while waiting:
            self.brain.run_program(inputs=inputs)
            direction = self.brain.screen_output.pop()
            color = self.brain.screen_output.pop()
            self.paint(color)
            self.turn(direction)
            self.move()
            inputs = [self.get_color()]
            waiting = self.brain.waiting

    def turn(self, direction):
        if direction == self.DIR_COUNTER_CLOCKWISE:
            self.direction[1] *= -1
            self.direction.reverse()
        elif direction == self.DIR_CLOCKWISE:
            self.direction[0] *= -1
            self.direction.reverse()
        else:
            raise ValueError(
                f"turn direction must be one of {','.join((self.DIR_COUNTER_CLOCKWISE, self.DIR_CLOCKWISE))} - got {direction}"
            )

    def move(self):
        self.position = list(map(add, self.position, self.direction))

    def paint(self, color):
        if color not in (self.COL_BLACK, self.COL_WHITE):
            raise ValueError(
                f"paint color must be one of {','.join((self.COL_BLACK, self.COL_WHITE))} - got {color}"
            )
        self.painted_positions[Point(*self.position)] = color

    def get_color(self):
        return self.painted_positions.get(Point(*self.position), self.COL_BLACK)

    @property
    def hull(self):
        minx = min(point.x for point in self.painted_positions)
        miny = min(point.y for point in self.painted_positions)
        if minx < 0:
            xoffset = -minx
        elif minx == 0:
            xoffset = 0
        elif minx > 0:
            xoffset = minx
        if miny < 0:
            yoffset = -miny
        elif miny == 0:
            yoffset = 0
        elif miny > 0:
            yoffset = miny
        maxx = max(point.x + xoffset for point in self.painted_positions)
        maxy = max(point.y + yoffset for point in self.painted_positions)
        new_positions = {Point(p.x+xoffset, p.y+yoffset): c for p, c in self.painted_positions.items()}
        out = []
        for y in range(maxy+1, -1, -1):
            row = ""
            for x in range(maxx+1):
                row += COLORS[new_positions.get(Point(x, y), self.COL_BLACK)]
            out.append(row)
        return out


def phase1(data):
    robot = HullPaintingRobot(program=data)
    robot.go()
    return len(robot.painted_positions)


def phase2(data):
    robot = HullPaintingRobot(program=data, start_on_white=True)
    robot.go()
    return "\n"+("\n".join(line for line in robot.hull))


solution = Solution(2019, 11, phase2=phase2, input_parser=IntCode.read_code)
