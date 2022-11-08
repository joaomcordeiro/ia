import cl_node as node
import GlobalVariables as gv

def Dijkstra():
    global path_found

    source = matrix[source_coords[0], source_coords[1]]
    unvisited = [source]

    path_found = False

    while unvisited:
        if path_found:
            highlight_path()
            break

        nearest_node = heapq.heappop(unvisited)
        distance_from_start = nearest_node.distance_from_start + 1

        neighbours = find_neighbours(nearest_node.coords)

        for neighbour in neighbours:
            if neighbour and not neighbour.is_visited and not neighbour.is_wall:
                heapq.heappush(unvisited, neighbour)
                mark_as_visited(neighbour, nearest_node, distance_from_start)

    if not unvisited or not path_found:
        print('THERE IS NO PATH')


def ASearch():
    global path_found

    source = matrix[source_coords[0], source_coords[1]]
    destination = matrix[destination_coords[0], destination_coords[1]]

    source.g = 0
    source.h = calculate_manhattan_distance(source, destination)
    source.f = source.g + source.h

    count = 0
    unvisited = PriorityQueue()
    unvisited.put((0, count, source))

    path_found = False

    while unvisited:
        if path_found:
            highlight_path()
            break

        nearest_node = unvisited.get()[2]

        neighbours = find_neighbours(nearest_node.coords)

        for neighbour in neighbours:

            if neighbour and not neighbour.is_wall:
                tmp_g = calculate_manhattan_distance(neighbour, source)

                if tmp_g < neighbour.g:
                    tmp_h = calculate_manhattan_distance(
                        neighbour, destination)
                    tmp_f = tmp_g + tmp_h

                    if not neighbour.is_visited:
                        mark_as_visited(neighbour, nearest_node,
                                        tmp_f, tmp_g, tmp_h)
                        count += 1
                        unvisited.put((neighbour.f, count, neighbour))

    if not unvisited or not path_found:
        print('THERE IS NO PATH')


def BFS():
    global path_found

    source = matrix[source_coords[0], source_coords[1]]
    destination = matrix[destination_coords[0], destination_coords[1]]

    unvisited = [source]

    path_found = False

    while unvisited:
        if path_found:
            highlight_path()
            break

        nearest_node = unvisited.pop(0)

        neighbours = find_neighbours(nearest_node.coords)

        for neighbour in neighbours:
            if neighbour and not neighbour.is_visited and not neighbour.is_wall:

                if neighbour not in unvisited:
                    heapq.heappush(unvisited, neighbour)
                    mark_as_visited(neighbour, predecessor=nearest_node)

    if not unvisited or not path_found:
        print('THERE IS NO PATH')


def DFS():
    global path_found

    source = matrix[source_coords[0], source_coords[1]]
    destination = matrix[destination_coords[0], destination_coords[1]]

    unvisited = [source]

    path_found = False

    while unvisited:
        if path_found:
            highlight_path()
            break

        nearest_node = unvisited.pop()

        neighbours = find_neighbours(nearest_node.coords)

        for neighbour in neighbours:
            if neighbour and not neighbour.is_visited and not neighbour.is_wall:
                if neighbour not in unvisited:
                    heapq.heappush(unvisited, neighbour)
                    mark_as_visited(neighbour, predecessor=nearest_node)

    if not unvisited or not path_found:
        print('THERE IS NO PATH')


def find_neighbours(coords):
    """
    Finds the neighbours of the cell at given matrix coords
    """
    y, x = coords

    left_node = None
    if 0 <= x-1:
        left_node = matrix[y][x-1]

    right_node = None
    if x+1 < COLUMNS:
        right_node = matrix[y][x+1]

    upper_node = None
    if 0 <= y-1:
        upper_node = matrix[y-1][x]

    lower_node = None
    if y+1 < ROWS:
        lower_node = matrix[y+1][x]

    return [left_node, right_node, upper_node, lower_node]


def calculate_manhattan_distance(first_node, second_node):
    """
    Calculates the manhattan distance between 2 nodes
    """
    return abs(first_node.coords[0] - second_node.coords[0]) + abs(first_node.coords[1] - second_node.coords[1])


def mark_as_visited(node: node.Node, predecessor, distance=None, g=None, h=None):
    """
    Marks the given node as visited
    """
    global destination_coords, path_found

    node.is_visited = True

    if gv.algo_selection.get() == 'Dijkstra':
        if distance < node.distance_from_start:
            node.distance_from_start = distance
            node.predecessor = predecessor

    if gv.algo_selection.get() == 'ASearch':
        node.g = g
        node.h = h
        node.f = g+h
        node.predecessor = predecessor

    if gv.algo_selection.get() == 'BFS':
        node.predecessor = predecessor

    if gv.algo_selection.get() == 'DFS':
        node.predecessor = predecessor

    if node.coords != destination_coords:
        rect = node.shape
        pygame.draw.rect(screen, VISITED, rect)

        pygame.display.update()
    else:
        path_found = True
