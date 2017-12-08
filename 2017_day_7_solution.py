from utils import get_input
from collections import namedtuple

FlatNode = namedtuple("FlatNode", "name weight children")


def get_weight(node):
    weight = node["weight"]
    if node["children"] is not None:
        for child in node["children"]:
            weight += get_weight(node["children"][child])
    return weight


def get_imbalance(tree):
    weights_names = {node: get_weight(tree["children"][node]) for node in tree["children"]}
    weights = [get_weight(tree["children"][node]) for node in tree["children"]]
    weightset = set(weights)
    if len(weightset) == 1:
        return get_imbalance(tree["children"])
    for v in weights:
        if weights.count(v) == 1:
            outlier = v
        else:
            norm = v
    for k in weights_names:
        if weights_names[k] == outlier:
            wname = k
    return tree["children"][wname]["weight"] + (norm - outlier)


def get_parent(name, flat_list):
    for node in flat_list:
        if node.children is not None and name in node.children:
            return node.name
    return None


def make_association_dict(flat_list):
    output = {}
    for node in flat_list:
        output[node.name] = {"parent": get_parent(node.name, flat_list), "children": node.children, "weight": node.weight}
    return output


def unflatten(node_name, association_dict):
    n = association_dict[node_name]
    node_dict = {"weight": n["weight"], "children":None}
    if n["children"] is not None:
        node_dict["children"] = {child: unflatten(child, association_dict) for child in n["children"]}
    return node_dict


def build_tree(association_dict):
    for name in association_dict:
        if association_dict[name]["parent"] is None:
            tree = {name: unflatten(name, association_dict)}
    return tree


def parse_input(input):
    for raw_data in input:
        children = None
        if "->" in raw_data:
            raw_data, children_str = raw_data.split("->")
            children = [c.strip() for c in children_str.split(',')]
        name, raw_weight = raw_data.split()
        weight = int(raw_weight.lstrip('(').rstrip(')'))

        yield FlatNode(name.strip(), weight, children)

def solution_7_1(input):
    tree = build_tree(make_association_dict(list(input)))
    return list(tree.keys())[0]


def solution_7_2(input):
    tree = build_tree(make_association_dict(list(input)))
    return get_imbalance(tree[list(tree.keys())[0]])


if __name__ == '__main__':

    print(solution_7_1(parse_input(get_input(2017, 7))))
    print(solution_7_2(parse_input(get_input(2017, 7))))