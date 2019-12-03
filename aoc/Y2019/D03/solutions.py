from ...classes import Solution
from collections import namedtuple
from typing import List, Iterator

PathItem = namedtuple("PathItem", "direction size")
Point = namedtuple("Point", "x y")

DIRECTIONS = {
    "L": {"axis": "x", "op": "-"},
    "R": {"axis": "x", "op": "+"},
    "U": {"axis": "y", "op": "+"},
    "D": {"axis": "y", "op": "-"},
}


def parse_input(data: List[str]) -> List[List[PathItem]]:
    output = []
    for line in data:
        line = line.strip()
        pathitems = line.split(',')
        output.append([PathItem(i[0], int(i[1:])) for i in pathitems])
    return output


def iter_path_points(items: List[List[PathItem]]) -> Iterator[Point]:
    """
    Yields all points a path is going through.
    """
    position = Point(0, 0)
    for item in items:
        changes = DIRECTIONS[item.direction]
        for n in range(1, item.size + 1):
            args = {"x": position.x, "y": position.y}
            if changes["op"] == "+":
                args[changes["axis"]] += 1
            elif changes["op"] == "-":
                args[changes["axis"]] -= 1
            position = Point(**args)
            yield position


def manhattan(p1: Point, p2: Point) -> int:
    """
    Returns the Manhattan distance between two Points.
    """
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def get_intersections(data: List[List[PathItem]]):
    """
    Returns the coordinates of paths intersections.
    """
    path1 = set(iter_path_points(data[0]))
    path2 = set(iter_path_points(data[1]))

    return path1.intersection(path2)


def phase1(data):
    intersections = get_intersections(data)

    return min(manhattan(Point(0, 0), p) for p in intersections)


def phase2(data):
    path1 = list(iter_path_points(data[0]))
    path2 = list(iter_path_points(data[1]))
    intersections = get_intersections(data)
    intersection_costs = []
    for intersection in intersections:
        # add 2 because iter_path_points doesn't yield the origin
        cost = path1.index(intersection) + path2.index(intersection) + 2
        intersection_costs.append(cost)
    return min(intersection_costs)


solution = Solution(2019, 3, phase1=phase1, phase2=phase2, input_parser=parse_input)
