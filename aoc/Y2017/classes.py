import collections


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

    def connected_components(self):
        out = []
        nodes = set(self.edges.keys())
        visited = set()
        while len(nodes):
            node = nodes.pop()
            connected = set()
            queue = Queue()
            queue.put(node)
            if node not in visited:
                while not queue.empty():
                    n = queue.get()
                    for neighbor in self.neighbors(n):
                        if neighbor not in connected:
                            queue.put(neighbor)
                    connected.add(n)
                    visited.add(n)
                out.append(connected)
        return out

    def has_path(self, start, goal):
        if start == goal:
            return True
        elif goal not in self.edges:
            return False
        path = self.breadth_first_search(start, goal)
        if goal in path:
            return True
        return False

    def get_path(self, node, start):
        out = [node]
        current = node
        while current != start:
            current = self.came_from[current]
            out.append(current)
        out.reverse()
        return out