from utils import get_input, Graph


def parse_input(input):
    output = {}
    for line in input:
        node, edges = line.split(' <-> ')
        output[node] = set(edge.strip() for edge in edges.split(', '))
    return output


def consolidate_graph(data):
    for node, edges in data.items():
        for edge in edges:
            data[edge].add(node)
        return data


def solution_12_1(input):
    g = Graph()
    g.edges = consolidate_graph(input)
    res = [n for n in g.edges if g.has_path(n, '0')]
    return len(res)


def solution_12_2(input):
    g = Graph()
    g.edges = consolidate_graph(input)
    return len(g.connected_components())


if __name__ == '__main__':
    print(solution_12_1(parse_input(get_input(2017, 12))))
    print(solution_12_2(parse_input(get_input(2017, 12))))