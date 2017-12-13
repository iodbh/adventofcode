from ...classes import Solution
from ..classes import Graph


def parse_input(data):
    output = {}
    for line in data:
        node, edges = line.split(' <-> ')
        output[node] = set(edge.strip() for edge in edges.split(', '))
    return output


def consolidate_graph(data):
    for node, edges in data.items():
        for edge in edges:
            data[edge].add(node)
        return data


def phase1(data):
    g = Graph()
    g.edges = consolidate_graph(data)
    res = [n for n in g.edges if g.has_path(n, '0')]
    return len(res)


def phase2(data):
    g = Graph()
    g.edges = consolidate_graph(data)
    return len(g.connected_components())


solution = Solution(2017, 12, phase1=phase1, phase2=phase2, input_parser=parse_input)