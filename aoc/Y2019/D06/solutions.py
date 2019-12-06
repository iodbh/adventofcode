from ...classes import Solution
from collections import namedtuple
from copy import copy

Orbit = namedtuple("Orbit", "parent child")


def parse_data(data):
    return tuple(Orbit(*l.strip().split(")")) for l in data)


def build_tree(data):
    tree = {}
    for node in data:
        if node.parent not in tree:
            tree[node.parent] = {"children": {node.child}, "parent": None}
        else:
            tree[node.parent]["children"].add(node.child)
        if node.child not in tree:
            tree[node.child] = {"children": set(), "parent": node.parent}
        else:
            tree[node.child]["parent"] = node.parent
    return tree


def recurse_orbits(tree, node, depth=0):
    count = 0
    for child in tree[node]["children"]:
        count += 1 + depth
        if child in tree:
            count += recurse_orbits(tree, child, depth+1)
    return count


def iter_edges(node_data):
    if node_data["parent"] is not None:
        yield node_data["parent"]
    for child in node_data["children"]:
        yield child


def shortest_path(tree: dict, frontier: set, destination: str, transfers: int = 0):
    for origin in copy(frontier):
        if origin == destination:
            return transfers
        frontier.remove(origin)
        for edge in iter_edges(tree[origin]):
            frontier.add(edge)
    transfers += 1
    return shortest_path(tree, frontier, destination, transfers=transfers)


def phase1(data):
    tree = build_tree(data)
    return recurse_orbits(tree, "COM")


def phase2(data):
    tree = build_tree(data)
    try:
        origin = tree["YOU"]["parent"]
        destination = tree["SAN"]["parent"]
    except KeyError:
        raise ValueError('"YOU" or "SAN" orbit missing from data. (they\'re not in the test input)')
    return shortest_path(tree, {origin}, destination)


solution = Solution(2019, 6, phase1=phase1, phase2=phase2, input_parser=parse_data)
