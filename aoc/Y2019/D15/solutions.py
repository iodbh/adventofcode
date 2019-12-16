from ...classes import Solution
from ..classes import IntCode, Screen
from ...Y2017.classes import Graph, Queue
from collections import namedtuple
import curses
from time import sleep

Point = namedtuple("Point", "x y")


class RepairDroid:

    DIRECTIONS = {
        "N": {"command": 1, "opposite": "S", "mask": (0, 1)},
        "S": {"command": 2, "opposite": "N", "mask": (0, -1)},
        "W": {"command": 3, "opposite": "E", "mask": (-1, 0)},
        "E": {"command": 4, "opposite": "W", "mask": (1, 0)},
    }

    MASKS = {item["mask"]: key for key, item in DIRECTIONS.items()}

    TILES = {
        0: {"str": "  ", "colors": 1, "name": "wall"},
        1: {"str": "  ", "name": "empty"},
        2: {"str": "  ", "colors": 2, "name": "target"},
        3: {"str": "  ", "colors": 3, "name": "robot"},
        4: {"str": "  ", "colors": 4, "name": "origin"},
    }

    COLORS = {
        1: (curses.COLOR_WHITE, curses.COLOR_WHITE),
        2: (curses.COLOR_GREEN, curses.COLOR_GREEN),
        3: (curses.COLOR_RED, curses.COLOR_RED),
        4: (curses.COLOR_YELLOW, curses.COLOR_YELLOW),
    }

    def __init__(self, program, scr=None, delay=0):
        """
        delay will be passed to time.sleep() after each move (to make the
        visulization more readable).

        if scr is a curses window, the visualization will be rendered.
        """
        self.cpu = IntCode(program, silent=True, input_wait=True)
        self.map = Graph()
        self.display = False
        self.delay = delay
        if scr is not None:
            self.screen = Screen(50, 50, self.TILES, scr=scr, colors=self.COLORS)
            self.display = True
        self.position = Point(0, 0)
        self.map.edges[self.position] = []
        self.grid = {0: {self.position}, 1: set(), 2: set()}

    def move(self, direction):
        """
        Move one cell in the given direction.
        """
        command = self.DIRECTIONS[direction]["command"]
        mem, out = self.cpu.run_program(inputs=[command])
        status = out.pop()
        if status in (1, 2):
            self.position = Point(
                self.position.x + self.DIRECTIONS[direction]["mask"][0],
                self.position.y + self.DIRECTIONS[direction]["mask"][1]
            )
        if self.display:
            self.draw_grid()
        sleep(self.delay)
        return status

    def move_to(self, target):
        """
        Find the shortest path to the target cell and move there.
        """
        self.map.breadth_first_search(self.position, target)
        path = self.map.get_path(target, self.position)
        for node in path[1:]:
            mask = (
                node.x - self.position.x,
                node.y - self.position.y
            )
            direction = self.MASKS[mask]
            self.move(direction)

    def add_node(self, node, parent):
        """
        Add an edge to the map graph.
        """
        if node not in self.map.edges:
            self.map.edges[node] = []
        if parent not in self.map.edges:
            self.map.edges[parent] = [node]
        else:
            self.map.edges[parent].append(node)

    def _check_neighbors(self):
        """
        Move in each direction and yield its coordinates if it's not a wall.
        """
        for direction, dir_info in self.DIRECTIONS.items():
            pos = Point(
                self.position.x + dir_info["mask"][0],
                self.position.y + dir_info["mask"][1]
            )
            status = self.move(direction)
            self.grid[status].add(pos)
            if status in (1, 2):
                # moved
                self.move(dir_info["opposite"])
                yield pos

    def discover_map(self):
        """
        Explore the map and populate the map graph. The order of visited cells
        still needs to be optimized to minimize the amount of movement required.
        """
        frontier = Queue()
        cleared = {self.position}
        for pos in self._check_neighbors():
            frontier.put(pos)
            self.add_node(pos, self.position)
        while not frontier.empty():
            next = frontier.get()
            if next not in cleared:
                self.move_to(next)
                for pos in self._check_neighbors():
                    self.add_node(pos, self.position)
                    frontier.put(pos)
            cleared.add(self.position)

        return tuple(self.grid[2])[0]

    def draw_grid(self):
        """
        Render the map with curses.
        """
        self.screen.draw_many_tiles(tile for tile in self.iter_grid_tiles())
        pass

    def iter_grid_tiles(self):
        """
        converts the coordinates from relative to absolute and yields tiles to
        be rendered by the screen.
        """
        all_points = self.grid[0].union(self.grid[1], self.grid[2], {self.position})
        min_x = min(p.x for p in all_points)
        min_y = min(p.y for p in all_points)

        if min_x < 0:
            xoffset = -min_x
        elif min_x == 0:
            xoffset = 0
        elif min_x > 0:
            xoffset = min_x
        if min_y < 0:
            yoffset = -min_y
        elif min_y == 0:
            yoffset = 0
        elif min_y > 0:
            yoffset = min_y
        origin = Point(0 + xoffset, 0 + yoffset)
        position = Point(self.position.x + xoffset, self.position.y + yoffset)
        for tile_type in (0, 1, 2):
            for point in self.grid[tile_type]:
                newpoint = Point(point.x + xoffset, point.y + yoffset)
                if newpoint not in (origin, position):
                    yield newpoint.x, newpoint.y, tile_type
        yield origin.x, origin.y , 4
        yield position.x, position.y, 3


def p1_viz(scr, data):
    robot = RepairDroid(data, scr=scr, delay=0.3)
    robot.discover_map()
    while True:
        pass


def p1_nodispp(data):
    robot = RepairDroid(data)
    target = robot.discover_map()
    robot.map.breadth_first_search(Point(0, 0), target)
    path = robot.map.get_path(target, Point(0, 0))
    return len(path[1:])


def phase1(data):
    #curses.wrapper(p1_viz, data)
    return p1_nodispp(data)


def phase2(data):
    robot = RepairDroid(data)
    source = robot.discover_map()
    max_cost = 0
    for cell in robot.grid[1]:
        robot.map.breadth_first_search(source, cell)
        path = robot.map.get_path(cell, source)
        cost = len(path[1:])
        if cost > max_cost:
            max_cost = cost
    return max_cost


solution = Solution(2019, 15, phase1=phase1, phase2=phase2, input_parser=IntCode.read_code)
