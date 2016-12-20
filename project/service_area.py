import bin
import dijkstra

""" The area class contains the road layout dictionary, a lorry and bins """


class Area:
    def __init__(self, area_id, service_frequency, threshold, bins, bin_volume, lorry, route_map):
        self.area_id = area_id
        self.service_frequency = 1.0 / service_frequency
        self.lorry = lorry
        self.bins = {}
        for i in range(1, int(bins + 1)):
            a_bin = bin.Bin(bin_volume, self.area_id, i, threshold)
            self.bins[i] = a_bin
        self.distance_map = convert_road_matrix_to_distance_dict(route_map)

        # self.overflown_bins = 0
        self.full_bins = 0
        self.empty_bins = 0

    def schedule_service(self):
        self.lorry.schedule_task()
        # maybe do stuff here


def convert_road_matrix_to_distance_dict(route_map):
    graph = dijkstra.Graph()
    distance_dict = {}

    for node in range(0, len(route_map)):
        graph.add_node(node)
    for start_node in range(0, len(route_map)):
        for end_node in range(0, len(route_map)):
            distance = route_map[start_node][end_node]
            if distance >= 0:
                graph.add_edge(start_node, end_node, distance)
    for node in graph.nodes:
        distance_dict[node] = dijkstra.dijkstra(graph, node)
    return distance_dict
