from enum import Enum
import numpy as np
import pygame
import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog
import os
import platform
import heapq
from queue import PriorityQueue
import json
from cl_tkWindow import *
from cl_enum import *
from cl_node import *

EDITING_MODES = Enum(["SOURCE", "DESTINATION", "WALL", "ERASE"])

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

CELL_SIZE = 20
MARGIN = 1
ROWS = 25
COLUMNS = 25

WINDOW_WIDTH = COLUMNS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

CELL = (255, 255, 255)
WALL = (128, 128, 128)
CELL_BORDER = (172, 172, 172)
SOURCE = (0, 220, 0)
DESTINATION = (237, 67, 0)
VISITED = (198, 255, 255)
PATH = (251, 255, 100)

LC_CELL = (255, 255, 255)
LC_WALL = (128, 128, 128)
LC_CELL_BORDER = (172, 172, 172)
LC_SOURCE = (0, 220, 0)
LC_DESTINATION = (237, 67, 0)
LC_VISITED = (198, 255, 255)
LC_PATH = (251, 255, 100)

HC_CELL = (192, 192, 192)
HC_WALL = (0, 0, 0)
HC_CELL_BORDER = (0, 0, 0)
HC_SOURCE = (0, 0, 255)
HC_DESTINATION = (255, 0, 0)
HC_VISITED = (255, 255, 255)
HC_PATH = (114, 255, 209)


def close():
    """
    Closes the program
    """
    global running, pygame_started
    running = False
    pygame_started = False
    pygame.quit()


"""
Settings Window (Tkinter)
"""
root = tk.Tk()
root.protocol('WM_DELETE_WINDOW', close)

"""
Grid Window (PyGame)
"""
screen = None

current_mode = EDITING_MODES.SOURCE
edit_mode_rb = IntVar()

algo_selection = StringVar()

high_contrast_mode = BooleanVar()

matrix = None

source_coords = None
destination_coords = None

path_found = False

running = True
pygame_started = False

"""
true when holding down the mouse button
"""
holding = False


def check_for_events():
    """
    Listens for events inside of the pygame window
    """
    global pygame_started, holding, screen

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame_started = False
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame_started = False
                pygame.quit()

            if event.key == K_RETURN:
                place_random_nodes()

            if event.key == K_BACKSPACE:
                reset_last_grid()

        if event.type == MOUSEBUTTONDOWN:
            mark_cell()
            holding = True

        if event.type == MOUSEBUTTONUP:
            holding = False

        if event.type == MOUSEMOTION and holding:
            mark_cell()


def find_path():
    """
    Finds the path using the selected algorithm
    """

    global pygame_started, path_found

    if not pygame_started:
        init_pygame()
        return

    if path_found:
        reset_last_grid()
        path_found = False

    if source_coords and destination_coords:

        if algo_selection.get() == 'Dijkstra':
            Dijkstra()

        if algo_selection.get() == 'ASearch':
            ASearch()

        if algo_selection.get() == 'BFS':
            BFS()

        if algo_selection.get() == 'DFS':
            DFS()


def highlight_path():
    """
    Highlights the path
    """
    global destination_coords, source_coords

    path_lenght = 0

    current = matrix[destination_coords[0], destination_coords[1]].predecessor
    source_node = matrix[source_coords[0], source_coords[1]]

    while current != source_node:
        rect = current.shape
        pygame.draw.rect(screen, PATH, rect)

        pygame.display.update()

        current = current.predecessor

        path_lenght += 1

    print(path_lenght)


def init_grid():
    """
    Initializes the grid into the pygame window
    """
    global screen, matrix, source_coords, destination_coords
    PADDING = (WINDOW_WIDTH - MARGIN * COLUMNS) // COLUMNS

    if source_coords and (source_coords[0] >= ROWS or source_coords[1] >= COLUMNS):
        source_coords = None

    if destination_coords and (destination_coords[0] >= ROWS or destination_coords[1] >= COLUMNS):
        destination_coords = None

    for y in range(ROWS):
        for x in range(COLUMNS):
            shape = pygame.Rect(
                (MARGIN + PADDING) * x + MARGIN,
                (MARGIN + PADDING) * y + MARGIN,
                PADDING,
                PADDING,
            )
            pygame.draw.rect(screen, CELL, shape)
            matrix[y][x] = Node(coords=(y, x),
                                shape=shape.copy())


def init_matrix():
    """
    Returns a bidimensional matrix
    """
    return np.empty((ROWS, COLUMNS), dtype=Node)


def init_pygame():
    """
    Starts the pygame window
    """
    global pygame_started, matrix, screen

    if screen:
        pygame_started = False
        pygame.quit()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill(CELL_BORDER)
    pygame.display.set_caption('Pathfinder')

    pygame.display.init()

    pygame.display.update()

    path_found = False

    matrix = init_matrix()
    init_grid()
    pygame.display.update()

    pygame_started = True


def init_settings_window():
    """
    Starts the settings window
    """
    settings_win = TkWindow(root)


def load_grid():
    """
    Loads grid-datas from file and starts the pygame windows
    """
    global source_coords, destination_coords, matrix
    fd = filedialog.askopenfilename(
        initialdir='grid_saves', initialfile='grid0.dat')
    if fd:
        f = open(fd, 'r')
        if f:
            text = f.read()
            f.close()
            decoded = json.loads(text)

            rows = decoded['rows']
            cols = decoded['columns']
            cell_size = decoded['cell_size']

            refresh_rows_cols(rows, cols, cell_size)

            source_coords = decoded['source_coords']
            destination_coords = decoded['destination_coords']

            walls = decoded['walls']

            init_pygame()

            """
            Drawing the walls
            """
            for wall in walls:
                wall_coords = wall
                wall_cell = matrix[wall_coords[0], wall_coords[1]]
                rect = wall_cell.shape
                pygame.draw.rect(screen, WALL, rect)
                wall_cell.is_wall = True

            pygame.display.update()

            """
            Drawing the destination
            """
            if destination_coords:
                destination_cell = matrix[destination_coords[0],
                                          destination_coords[1]]
                pygame.draw.rect(screen, DESTINATION, destination_cell.shape)
                matrix[destination_coords[0], destination_coords[1]] = Node(
                    destination_coords, destination_cell.shape.copy())

            """
            Drawing the source
            """
            if source_coords:
                source_cell = matrix[source_coords[0], source_coords[1]]
                pygame.draw.rect(screen, SOURCE, source_cell.shape)
                matrix[source_coords[0], source_coords[1]] = Node(source_coords, source_cell.shape.copy(),
                                                                  distance_from_start=0, is_wall=True, is_visited=True,
                                                                  predecessor=None)

            pygame.display.update()


def mark_cell():
    """
    Marks the cell hovered by the mouse cursor
    """
    global matrix, screen, source_coords, destination_coords
    coords = pygame.mouse.get_pos()
    x = coords[1] // CELL_SIZE
    y = coords[0] // CELL_SIZE

    hover_node = matrix[x][y]

    """
    SOURCE CELL MODE
    """
    if current_mode == EDITING_MODES.SOURCE:
        if hover_node.coords is not source_coords and hover_node.coords is not destination_coords:
            source_cell = None

            """
            If there is no Source node it initializes it, overwrites instead
            """
            if source_coords is None:
                source_coords = x, y
            else:
                source_cell = matrix[source_coords[0], source_coords[1]]
                pygame.draw.rect(screen, CELL, source_cell.shape)
                matrix[source_coords[0], source_coords[1]] = Node(source_coords, source_cell.shape.copy(),
                                                                  distance_from_start=np.inf,
                                                                  is_wall=False, is_visited=False, predecessor=None)
                source_coords = x, y

            source_cell = matrix[source_coords[0], source_coords[1]]

            pygame.draw.rect(screen, SOURCE, source_cell.shape)
            matrix[source_coords[0], source_coords[1]] = Node(source_coords, source_cell.shape.copy(),
                                                              distance_from_start=0,
                                                              is_wall=True, is_visited=True, predecessor=None)

    """
    DESTINATION CELL MODE
    """
    if current_mode == EDITING_MODES.DESTINATION:
        if hover_node.coords is not source_coords and hover_node.coords is not destination_coords:
            destination_cell = None

            """
            If there is no Destination node it initializes it, overwrites instead
            """
            if destination_coords is None:
                destination_coords = x, y
            else:
                destination_cell = matrix[destination_coords[0],
                                          destination_coords[1]]
                pygame.draw.rect(screen, CELL, destination_cell.shape)

                matrix[destination_coords[0], destination_coords[1]] = Node(
                    destination_coords, destination_cell.shape.copy())

                destination_coords = x, y

            destination_cell = matrix[destination_coords[0],
                                      destination_coords[1]]

            pygame.draw.rect(screen, DESTINATION, destination_cell.shape)
            matrix[destination_coords[0], destination_coords[1]] = Node(
                destination_coords, destination_cell.shape.copy())

    """
    WALL CELL MODE
    """
    if current_mode == EDITING_MODES.WALL:
        if hover_node.coords is not source_coords and hover_node.coords is not destination_coords:
            hover_node.is_wall = True
            rect = hover_node.shape
            pygame.draw.rect(screen, WALL, rect)

    """
    ERASE CELL MODE
    """
    if current_mode == EDITING_MODES.ERASE:
        if hover_node.coords is not source_coords and hover_node.coords is not destination_coords:
            pygame.draw.rect(screen, CELL, hover_node.shape)
            matrix[hover_node.coords[0], hover_node.coords[1]] = Node(hover_node.coords, hover_node.shape.copy(),
                                                                      distance_from_start=np.inf,
                                                                      is_wall=False, is_visited=False, predecessor=None)

    pygame.display.update()


def place_random_nodes():
    global source_coords, destination_coords

    init_grid()

    source_coords = (np.random.randint(0, ROWS),
                     np.random.randint(0, COLUMNS))
    destination_coords = (np.random.randint(0, ROWS),
                          np.random.randint(0, COLUMNS))

    while source_coords == destination_coords:
        destination_coords = (np.random.randint(0, ROWS),
                              np.random.randint(0, COLUMNS))

    reset_last_grid()


def reset_last_grid():
    global source_coords, destination_coords

    if not pygame_started:
        init_pygame()
        return

    walls = []
    for y in range(ROWS):
        for x in range(COLUMNS):
            if matrix[y][x].is_wall and matrix[y][x].coords != source_coords:
                walls.append((matrix[y][x].coords))

    _source_coords = source_coords
    _destination_coords = destination_coords

    init_pygame()

    source_coords = _source_coords
    destination_coords = _destination_coords

    for wall in walls:
        wall_coords = wall
        wall_cell = matrix[wall_coords[0], wall_coords[1]]
        rect = wall_cell.shape
        pygame.draw.rect(screen, WALL, rect)
        wall_cell.is_wall = True

    pygame.display.update()

    if destination_coords:
        destination_cell = matrix[destination_coords[0], destination_coords[1]]
        pygame.draw.rect(screen, DESTINATION, destination_cell.shape)
        matrix[destination_coords[0], destination_coords[1]] = Node(
            destination_coords, destination_cell.shape.copy())

    if source_coords:
        source_cell = matrix[source_coords[0], source_coords[1]]
        pygame.draw.rect(screen, SOURCE, source_cell.shape)
        matrix[source_coords[0], source_coords[1]] = Node(source_coords, source_cell.shape.copy(),
                                                          distance_from_start=0, is_wall=True, is_visited=True,
                                                          predecessor=None)

    pygame.display.update()


def set_contrast_mode():
    global source_coords, destination_coords, matrix, pygame_started

    global CELL, HC_CELL, LC_CELL
    global WALL, HC_WALL, LC_WALL
    global CELL_BORDER, HC_CELL_BORDER, LC_CELL_BORDER
    global SOURCE, HC_SOURCE, LC_SOURCE
    global DESTINATION, HC_DESTINATION, LC_DESTINATION
    global VISITED, HC_VISITED, LC_VISITED
    global PATH, HC_PATH, LC_PATH

    if high_contrast_mode.get():
        CELL = HC_CELL
        WALL = HC_WALL
        CELL_BORDER = HC_CELL_BORDER
        SOURCE = HC_SOURCE
        DESTINATION = HC_DESTINATION
        VISITED = HC_VISITED
        PATH = HC_PATH
    else:
        CELL = LC_CELL
        WALL = LC_WALL
        CELL_BORDER = LC_CELL_BORDER
        SOURCE = LC_SOURCE
        DESTINATION = LC_DESTINATION
        VISITED = LC_VISITED
        PATH = LC_PATH

    if pygame_started:
        reset_last_grid()


def refresh_rows_cols(rows, cols, cell_size):
    """
    Refreshs the values for rows, columns and cell size
    """

    global ROWS, COLUMNS, WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE

    if rows != 0:
        ROWS = rows

    if cols != 0:
        COLUMNS = cols

    if cell_size != 0:
        CELL_SIZE = cell_size

    WINDOW_WIDTH = COLUMNS * CELL_SIZE
    WINDOW_HEIGHT = ROWS * CELL_SIZE


def save_grid():
    """
    Saves grid-datas from file and starts the pygame windows
    """
    fd = filedialog.asksaveasfilename(
        initialdir='grid_saves', initialfile='grid0.dat')

    if fd:
        f = open(fd, 'w')
        if f:
            walls = []
            for y in range(ROWS):
                for x in range(COLUMNS):
                    if matrix[y][x].is_wall and matrix[y][x].coords != source_coords:
                        walls.append((matrix[y][x].coords))

            text = {"rows": ROWS, "columns": COLUMNS, "cell_size": CELL_SIZE, "source_coords": source_coords,
                    "destination_coords": destination_coords, "walls": walls}

            js = json.dumps(text)
            f.write(js)
            f.close()


def change_editing_mode():
    global edit_mode_rb, current_mode

    if edit_mode_rb.get() == 1:
        current_mode = EDITING_MODES.SOURCE
    if edit_mode_rb.get() == 2:
        current_mode = EDITING_MODES.DESTINATION
    if edit_mode_rb.get() == 3:
        current_mode = EDITING_MODES.WALL
    if edit_mode_rb.get() == 4:
        current_mode = EDITING_MODES.ERASE


def main():
    init_settings_window()

    while running:
        root.update()

        if pygame_started:
            check_for_events()

    root.destroy()


if __name__ == "__main__":
    main()
