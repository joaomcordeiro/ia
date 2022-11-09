import numpy as np
import GlobalVariables as gv


class Node:

    def __init__(self, coords, shape, distance_from_start=np.inf, is_wall=False, is_visited=False, is_encomenda=False,
                 predecessor=None,
                 f=np.inf, g=np.inf, h=np.inf):
        self.coords = coords
        self.shape = shape
        self.distance_from_start = distance_from_start
        self.is_wall = is_wall
        self.is_visited = is_visited
        self.is_encomenda = is_encomenda
        self.predecessor = predecessor
        self.f = f  # f-value for A Search
        self.g = g  # g-value for A Search
        self.h = h  # h-value for A Search

    def __lt__(self, node_to_check):
        # global algo_selection
        # global algo_selection

        # if gv.algo_selection.get() == 'Dijkstra':
        #     return self.distance_from_start < node_to_check.distance_from_start
        # elif gv.algo_selection.get() == 'ASearch':
        #     return self.f < node_to_check.f
        if gv.algo_selection == 'Dijkstra':
            return self.distance_from_start < node_to_check.distance_from_start
        elif gv.algo_selection == 'ASearch':
            return self.f < node_to_check.f
