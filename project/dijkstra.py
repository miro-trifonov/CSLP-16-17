from collections import defaultdict, deque

""" Dijkstra algorithm for graph traversal. "dijkstra" function returns for a point "a" the distance to all other points
    in a directed graph. Code taken from https://gist.github.com/mdsrosa/c71339cb23bc51e711d8,
    with slight modifications """


class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.distances[(from_node, to_node)] = distance


def dijkstra(graph, initial):
    visited = {initial: 0}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            try:
                weight = current_weight + graph.distances[(min_node, edge)]
                if weight < current_weight:
                    continue  # To take care of the -1 values
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight

    return visited
