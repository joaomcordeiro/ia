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
import GlobalVariables as gv
import cl_node as node
import cl_enum as enum
import datetime
# import algoritmos as al

from pygame.locals import QUIT, KEYDOWN, K_RETURN, K_ESCAPE, K_BACKSPACE, K_s, K_d, K_w, MOUSEBUTTONDOWN, MOUSEBUTTONUP, \
    MOUSEMOTION


class TkWindow:
    """
    Class used to handle the tkinter window
    """

    def __init__(self, win):
        global edit_mode_rb, high_contrast_mode

        #####   DECLARING LABELS AND ENTRIES   #####
        self.lbl_rows = Label(win, text='Largura:')
        self.lbl_cols = Label(win, text='Comprimento:')
        self.lbl_cell_size = Label(win, text='Tamanho da célula:')
        self.lbl_n_encomendas = Label(win, text='Nº de encomendas:')
        self.lbl_algo = Label(win, text='Algorithm:')
        self.lbl_veloc = Label(win, text='Velocidade')
        self.t_rows = Entry()
        self.t_rows.insert(END, str(HEIGHT))
        self.t_cols = Entry()
        self.t_cols.insert(END, str(WIDTH))
        self.t_cell_size = Entry()
        self.t_cell_size.insert(END, str(CELL_SIZE))
        self.t_n_encomendas = Entry()
        self.t_n_encomendas.insert(END, str(N_ENCOMENDAS))

        # gv.algo_selection.set('Dijkstra')
        gv.algo_selection = "Dijkstra"
        data = ('Dijkstra', 'ASearch', 'BFS', 'DFS')
        self.cb = Combobox(win, values=data)
        self.cb.bind('<<ComboboxSelected>>', self.change_algo_selection)
        self.cb.current(0)

        #####   RADIO BUTTONS    #####
        edit_mode_rb.set(1)
        self.lbl_editmode = Label(win, text='Editing Mode:')
        self.rb_src = Radiobutton(
            win, text='Robot', variable=edit_mode_rb, value=1, command=change_editing_mode)
        self.rb_dest = Radiobutton(
            win, text='Encomenda(s)', variable=edit_mode_rb, value=2, command=change_editing_mode)
        self.rb_wall = Radiobutton(
            win, text='Obstáculos', variable=edit_mode_rb, value=3, command=change_editing_mode)
        self.rb_erase = Radiobutton(
            win, text='Eliminar', variable=edit_mode_rb, value=4, command=change_editing_mode)
        self.rb_entrega = Radiobutton(
            win, text='Ponto de entrega', variable=edit_mode_rb, value=5, command=change_editing_mode)

        high_contrast_mode.set(False)
        self.cb_contrast_mode = Checkbutton(
            win, text="High Contrast", variable=high_contrast_mode, command=set_contrast_mode)

        #####   BUTTONS    #####
        self.btn_find = Button(win, text='Executar', command=find_path)
        self.btn_build_grid = Button(
            win, text='Desenhar Armazém', command=self.build_click)
        self.btn_reset_last_grid = Button(
            win, text='Reset Last', command=reset_last_grid)

        self.btn_load_grid = Button(win, text='Abrir Armazém', command=load_grid)
        self.btn_save_grid = Button(win, text='Guardar Armazém', command=save_grid)
        #####   PLACING #####

        self.lbl_rows.place(x=40, y=40)
        self.t_rows.place(x=160, y=40, width=50)
        self.lbl_cols.place(x=40, y=80)
        self.t_cols.place(x=160, y=80)
        self.lbl_cell_size.place(x=40, y=120)
        self.t_cell_size.place(x=160, y=120)
        self.lbl_n_encomendas.place(x=40, y=160)
        self.t_n_encomendas.place(x=160, y=160)
        self.lbl_algo.place(x=40, y=200)

        self.cb.place(x=160, y=200)

        self.lbl_editmode.place(x=40, y=240)
        self.rb_src.place(x=160, y=240)
        self.rb_dest.place(x=160, y=260)
        self.rb_wall.place(x=160, y=280)
        self.rb_entrega.place(x=160, y=300)
        self.rb_erase.place(x=160, y=320)

        self.btn_build_grid.place(x=40, y=360)
        # self.btn_reset_last_grid.place(x=160, y=340)
        self.btn_load_grid.place(x=40, y=400)
        self.btn_save_grid.place(x=40, y=440)
        self.btn_find.place(x=230, y=460)

        self.cb_contrast_mode.place(x=200, y=360)
        self.lbl_veloc.place(x=180, y=380)
        self.sld_veloc = Scale(from_=1, to=50, orient=HORIZONTAL)
        self.sld_veloc.set(20)
        self.sld_veloc.pack()
        self.sld_veloc.place(x=180, y=400)

        self.lbl_Estat = Label(win, text='Estatística')
        self.lbl_Estat.place(x=40, y=480)
        self.t_estat = Text(win, width=30, height=4)
        self.t_estat.place(x=40, y=500)

        root.title('Pathfinder Settings')
        root.geometry("350x600+10+10")

        os.environ['SDL_WINDOWID'] = str(root.winfo_id())
        if platform.system == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'

        os.environ['SDL_VIDEO_CENTERED'] = '0'

    def build_click(self):
        tmp_rows = int(self.t_rows.get())
        tmp_cols = int(self.t_cols.get())
        tmp_cell_size = int(self.t_cell_size.get())
        tmp_n_encomendas = int(self.t_n_encomendas.get())
        tmp_velocidade = int(self.sld_veloc.get())

        refresh_rows_cols(tmp_rows, tmp_cols, tmp_cell_size, tmp_n_encomendas, tmp_velocidade)
        init_pygame()

    def change_algo_selection(self, event):
        gv.algo_selection = self.cb.get()

    def setEstat(self, text):
        self.t_estat = text


EDITING_MODES = enum.Enum(["SOURCE", "DESTINATION", "WALL", "ERASE", "ENTREGA"])

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

CELL_SIZE = 25
MARGIN = 1
HEIGHT = 20
WIDTH = 20
N_ENCOMENDAS = 2

WINDOW_WIDTH = WIDTH * CELL_SIZE
WINDOW_HEIGHT = HEIGHT * CELL_SIZE

CELL = (255, 255, 255)
WALL = (128, 128, 128)
CELL_BORDER = (172, 172, 172)
SOURCE = (60, 90, 220)
DESTINATION = (60, 220, 90)
VISITED = (198, 255, 255)
PATH = (251, 255, 100)
ENTREGA = (210, 40, 20)

LC_CELL = (255, 255, 255)
LC_WALL = (128, 128, 128)
LC_CELL_BORDER = (172, 172, 172)
LC_SOURCE = (60, 90, 220)
LC_DESTINATION = (60, 220, 90)
LC_VISITED = (198, 255, 255)
LC_PATH = (251, 255, 100)
LC_ENTREGA = (210, 40, 20)

HC_CELL = (192, 192, 192)
HC_WALL = (0, 0, 0)
HC_CELL_BORDER = (0, 0, 0)
HC_SOURCE = (0, 0, 255)
HC_DESTINATION = (255, 0, 0)
HC_VISITED = (255, 255, 255)
HC_PATH = (114, 255, 209)
HC_ENTREGA = (255, 0, 0)


def close():
    """
    Closes the program
    """
    global running \
        # , pygame_started
    running = False
    gv.pygame_started = False
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

# algo_selection = StringVar()

high_contrast_mode = BooleanVar()

matrix = None

source_coords = None
destination_coords = None
entrega_coords = None
gv.totalEncomendas = 0
path_found = False

running = True
gv.pygame_started = False

"""
true when holding down the mouse button
"""
holding = False


def init_settings_window():
    """
    Starts the settings window
    """
    global settings_win
    settings_win = TkWindow(root)


def init_pygame():
    """
    Starts the pygame window
    """
    # global pygame_started, matrix, screen
    global matrix, screen
    matrix = None
    if screen:
        gv.pygame_started = False
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

    gv.pygame_started = True


def init_matrix():
    """
    Returns a bidimensional matrix
    """
    return np.empty((HEIGHT, WIDTH), dtype=node.Node)


def init_grid():
    """
    Initializes the grid into the pygame window
    """
    global screen, matrix, source_coords, destination_coords, entrega_coords
    PADDING = (WINDOW_WIDTH - MARGIN * WIDTH) // WIDTH

    if source_coords and (source_coords[0] >= HEIGHT or source_coords[1] >= WIDTH):
        source_coords = None

    # if destination_coords and (destination_coords[0] >= HEIGHT or destination_coords[1] >= WIDTH):
    #     destination_coords = None

    if entrega_coords and (entrega_coords[0] >= HEIGHT or entrega_coords[1] >= WIDTH):
        entrega_coords = None

    for y in range(HEIGHT):
        for x in range(WIDTH):
            shape = pygame.Rect(
                (MARGIN + PADDING) * x + MARGIN,
                (MARGIN + PADDING) * y + MARGIN,
                PADDING,
                PADDING,
            )
            pygame.draw.rect(screen, CELL, shape)
            matrix[y][x] = node.Node(coords=(y, x),
                                     shape=shape.copy())


def refresh_rows_cols(rows, cols, cell_size, n_encomendas, velocidade):
    """
    Refreshs the values for rows, columns and cell size
    """

    global HEIGHT, WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, N_ENCOMENDAS

    if rows != 0:
        HEIGHT = rows

    if cols != 0:
        WIDTH = cols

    if cell_size != 0:
        CELL_SIZE = cell_size

    if n_encomendas != 0:
        N_ENCOMENDAS = n_encomendas

    if velocidade != 0:
        gv.timeWait = velocidade

    WINDOW_WIDTH = WIDTH * CELL_SIZE
    WINDOW_HEIGHT = HEIGHT * CELL_SIZE


def reset_last_grid():
    global source_coords, destination_coords, entrega_coords

    if not gv.pygame_started:
        init_pygame()
        return

    walls = []
    encomendas = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if matrix[y][x].is_wall and matrix[y][x].coords != source_coords:
                walls.append((matrix[y][x].coords))
            if matrix[y][x].is_encomenda and matrix[y][x].coords != source_coords:
                encomendas.append((matrix[y][x].coords))

    _source_coords = source_coords
    _destination_coords = destination_coords
    _entrega_coords = entrega_coords

    init_pygame()

    source_coords = _source_coords
    destination_coords = _destination_coords
    entrega_coords = _entrega_coords

    for wall in walls:
        wall_coords = wall
        wall_cell = matrix[wall_coords[0], wall_coords[1]]
        rect = wall_cell.shape
        pygame.draw.rect(screen, WALL, rect)
        wall_cell.is_wall = True

    for encomenda in encomendas:
        encomenda_coords = encomenda
        encomenda_cell = matrix[encomenda_coords[0], encomenda_coords[1]]
        rect = encomenda_cell.shape
        pygame.draw.rect(screen, DESTINATION, rect)
        encomenda_cell.is_encomenda = True

    pygame.display.update()

    # if destination_coords:
    #     destination_cell = matrix[destination_coords[0], destination_coords[1]]
    #     pygame.draw.rect(screen, DESTINATION, destination_cell.shape)
    #     matrix[destination_coords[0], destination_coords[1]] = node.Node(
    #         destination_coords, destination_cell.shape.copy(), is_encomenda=True)

    if source_coords:
        source_cell = matrix[source_coords[0], source_coords[1]]
        pygame.draw.rect(screen, SOURCE, source_cell.shape)
        matrix[source_coords[0], source_coords[1]] = node.Node(source_coords, source_cell.shape.copy(),
                                                               distance_from_start=0, is_wall=True, is_visited=True,
                                                               is_encomenda=False, predecessor=None)

    if entrega_coords:
        entrega_cell = matrix[entrega_coords[0], entrega_coords[1]]
        pygame.draw.rect(screen, ENTREGA, entrega_cell.shape)
        matrix[entrega_coords[0], entrega_coords[1]] = node.Node(entrega_coords, entrega_cell.shape.copy(),
                                                                 distance_from_start=0, is_wall=False, is_visited=False,
                                                                 predecessor=None)

    pygame.display.update()


def load_grid():
    """
    Loads grid-datas from file and starts the pygame windows
    """
    global source_coords, destination_coords, matrix, entrega_coords
    gv.totalVisitados = 0
    fd = filedialog.askopenfilename(
        initialdir='grid_saves', initialfile='grid0.dat')
    gv.ultimoficheiroAberto = fd
    if fd:
        f = open(fd, 'r')
        if f:
            text = f.read()
            f.close()
            decoded = json.loads(text)

            rows = decoded['rows']
            cols = decoded['columns']
            cell_size = decoded['cell_size']
            n_encomendas = decoded['n_encomendas']
            velocidade = decoded['velocidade']
            gv.totalEncomendas = decoded['totalEncomendas']

            for y in range(HEIGHT):
                for x in range(WIDTH):
                    matrix[y][x] = None
                    # matrix[y][x] = node.Node((y,x), CELL, distance_from_start=np.inf,
                    #                          is_wall=False, is_visited=False,f=np.inf, g=np.inf, h=np.inf,
                    #                          is_encomenda=False,
                    #                          predecessor=None)

            refresh_rows_cols(rows, cols, cell_size, n_encomendas, velocidade)

            source_coords = decoded['source_coords']
            lstdestination_coords = decoded['svencomendas']
            entrega_coords = decoded['entrega_coords']

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

            for destination_coord in lstdestination_coords:
                encomenda_cell = matrix[destination_coord[0], destination_coord[1]]
                rect = encomenda_cell.shape
                pygame.draw.rect(screen, DESTINATION, rect)
                encomenda_cell.is_encomenda = True

            for co in lstdestination_coords:
                encomenda_cell = matrix[co[0], co[1]]
                matrix[co[0], co[1]] = node.Node(co, encomenda_cell.shape.copy(), distance_from_start=np.inf,
                                                 is_wall=False, is_visited=False, f=np.inf, g=np.inf, h=np.inf,
                                                 is_encomenda=True,
                                                 predecessor=None)
                gv.encomendas_coord.append(matrix[co[0], co[1]])

            pygame.display.update()

            """
            Drawing the destination
            """
            # if destination_coords:
            #     destination_cell = matrix[destination_coords[0],
            #                               destination_coords[1]]
            #     pygame.draw.rect(screen, DESTINATION, destination_cell.shape)
            #     matrix[destination_coords[0], destination_coords[1]] = node.Node(
            #         destination_coords, destination_cell.shape.copy())

            """
            Drawing the source
            """
            if source_coords:
                source_cell = matrix[source_coords[0], source_coords[1]]
                pygame.draw.rect(screen, SOURCE, source_cell.shape)
                matrix[source_coords[0], source_coords[1]] = node.Node(source_coords, source_cell.shape.copy(),
                                                                       distance_from_start=0, is_wall=True,
                                                                       is_visited=False,
                                                                       predecessor=None)
            """
            Drawing the Entrega point
            """
            if entrega_coords:
                entrega_cell = matrix[entrega_coords[0], entrega_coords[1]]
                pygame.draw.rect(screen, ENTREGA, entrega_cell.shape)
                matrix[entrega_coords[0], entrega_coords[1]] = node.Node(entrega_coords, entrega_cell.shape.copy(),
                                                                         distance_from_start=np.inf, is_wall=False,
                                                                         is_visited=False,
                                                                         predecessor=None)

            pygame.display.update()


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
            svencomendas = []
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    if matrix[y][x].is_wall and matrix[y][x].coords != source_coords:
                        walls.append((matrix[y][x].coords))
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    if matrix[y][x].is_encomenda and matrix[y][x].coords != source_coords:
                        svencomendas.append((matrix[y][x].coords))

            text = {"rows": HEIGHT, "columns": WIDTH, "cell_size": CELL_SIZE, "source_coords": source_coords,
                    "svencomendas": svencomendas, "walls": walls, "n_encomendas": N_ENCOMENDAS,
                    "entrega_coords": entrega_coords, "velocidade": gv.timeWait, "totalEncomendas": gv.totalEncomendas}

            js = json.dumps(text)
            f.write(js)
            f.close()


def save_stats():
    """
    Saves grid-datas from file and starts the pygame windows
    """
    # fd = filedialog.asksaveasfilename(
    #     initialdir='grid_saves', initialfile='stats.txt')
    # fd = filedialog.askopenfilename(initialdir='grid_saves', initialfile='stats.txt', mode)
    fd = "..\grid_saves\stats.csv"
    # fd = filedialog.askopenfile(initialdir='grid_saves', initialfile='stats.txt', mode='a')
    # fd = filedialog.askopenfile(initialdir='grid_saves', initialfile='stats.txt',mode='a+')

    if fd:
        f = open(fd, 'a+')
        if f:
            text = "\n" + str(gv.ultimoficheiroAberto)+","+str(gv.algo_selection)+","+ str(gv.totalVisitados)+","+str(gv.custoSolucao)+","+str(gv.tempoExecucao)

            # js = json.dumps(text)
            f.write(text)
            f.close()


def mark_cell():
    """
    Marks the cell hovered by the mouse cursor
    """
    global matrix, screen, source_coords, destination_coords, entrega_coords
    coords = pygame.mouse.get_pos()
    x = coords[1] // CELL_SIZE
    y = coords[0] // CELL_SIZE

    hover_node = matrix[x][y]

    """
    SOURCE CELL MODE - Onde esta o Robot
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
                matrix[source_coords[0], source_coords[1]] = node.Node(source_coords, source_cell.shape.copy(),
                                                                       distance_from_start=np.inf,
                                                                       is_wall=False, is_visited=False,
                                                                       is_encomenda=False, predecessor=None)
                source_coords = x, y

            source_cell = matrix[source_coords[0], source_coords[1]]
            pygame.draw.rect(screen, SOURCE, source_cell.shape)
            matrix[source_coords[0], source_coords[1]] = node.Node(source_coords, source_cell.shape.copy(),
                                                                   distance_from_start=0,
                                                                   is_wall=True, is_visited=True,
                                                                   is_encomenda=False, predecessor=None)

    """
    ENTREGA CELL MODE
    """
    if current_mode == EDITING_MODES.ENTREGA:
        if hover_node.coords is not source_coords and hover_node.coords is not destination_coords:
            entrega_cell = None

            """
            If there is no ENTREGA node it initializes it, overwrites instead
            """
            if entrega_coords is None:
                entrega_coords = x, y
            else:
                entrega_cell = matrix[entrega_coords[0], entrega_coords[1]]
                pygame.draw.rect(screen, CELL, entrega_cell.shape)
                matrix[entrega_coords[0], entrega_coords[1]] = node.Node(entrega_coords, entrega_cell.shape.copy(),
                                                                         distance_from_start=np.inf,
                                                                         is_wall=False, is_visited=False,
                                                                         is_encomenda=False,
                                                                         predecessor=None)
                entrega_coords = x, y

            entrega_cell = matrix[entrega_coords[0], entrega_coords[1]]
            pygame.draw.rect(screen, ENTREGA, entrega_cell.shape)
            matrix[entrega_coords[0], entrega_coords[1]] = node.Node(entrega_coords, entrega_cell.shape.copy(),
                                                                     distance_from_start=np.inf, is_encomenda=False,
                                                                     is_wall=False, is_visited=False, predecessor=None)

    """
    DESTINATION CELL MODE - Encomendas
    """
    if current_mode == EDITING_MODES.DESTINATION:
        if hover_node.coords is not source_coords and hover_node.coords is not entrega_coords:
            if hover_node.is_encomenda:
                gv.totalEncomendas -= 1
                pygame.draw.rect(screen, CELL, hover_node.shape)
                matrix[hover_node.coords[0], hover_node.coords[1]] = node.Node(hover_node.coords,
                                                                               hover_node.shape.copy(),
                                                                               distance_from_start=np.inf,
                                                                               is_wall=False, is_visited=False,
                                                                               predecessor=None)
                for co in range(len(gv.encomendas_coord) - 1):
                    if gv.encomendas_coord[co].coords == hover_node.coords: gv.encomendas_coord.pop(co)
            else:
                gv.totalEncomendas += 1
                rect = hover_node.shape
                pygame.draw.rect(screen, DESTINATION, rect)
                matrix[hover_node.coords[0], hover_node.coords[1]] = node.Node(hover_node.coords,
                                                                               hover_node.shape.copy(),
                                                                               distance_from_start=np.inf,
                                                                               is_wall=False, is_visited=False,
                                                                               is_encomenda=True,
                                                                               predecessor=None)
                gv.encomendas_coord.append(hover_node)

    """
    WALL CELL MODE
    """
    if current_mode == EDITING_MODES.WALL:
        if hover_node.coords is not source_coords and hover_node.coords is not destination_coords and hover_node.coords is not entrega_coords:
            if hover_node.is_wall:
                pygame.draw.rect(screen, CELL, hover_node.shape)
                matrix[hover_node.coords[0], hover_node.coords[1]] = node.Node(hover_node.coords,
                                                                               hover_node.shape.copy(),
                                                                               distance_from_start=np.inf,
                                                                               is_wall=False, is_visited=False,
                                                                               is_encomenda=False, predecessor=None)
            else:
                hover_node.is_wall = True
                rect = hover_node.shape
                pygame.draw.rect(screen, WALL, rect)

    """
    ERASE CELL MODE
    """

    if current_mode == EDITING_MODES.ERASE:
        if hover_node.coords is not source_coords and hover_node.coords is not destination_coords and hover_node.coords is not entrega_coords:
            pygame.draw.rect(screen, CELL, hover_node.shape)
            matrix[hover_node.coords[0], hover_node.coords[1]] = node.Node(hover_node.coords, hover_node.shape.copy(),
                                                                           distance_from_start=np.inf,
                                                                           is_wall=False, is_visited=False,
                                                                           predecessor=None)

    pygame.display.update()


def place_random_nodes():
    global source_coords, destination_coords

    init_grid()

    source_coords = (np.random.randint(0, HEIGHT),
                     np.random.randint(0, WIDTH))
    destination_coords = (np.random.randint(0, HEIGHT),
                          np.random.randint(0, WIDTH))

    while source_coords == destination_coords:
        destination_coords = (np.random.randint(0, HEIGHT),
                              np.random.randint(0, WIDTH))

    reset_last_grid()


# def find_best_candidate():


def find_path():
    """
    Finds the path using the selected algorithm
    """

    # global pygame_started, path_found
    global path_found, destination_coords, source_coords
    if not gv.pygame_started:
        init_pygame()
        return

    if path_found:
        reset_last_grid()
        path_found = False
    settings_win.t_estat.delete("1.0", "end")
    gv.totalVisitados = 0
    gv.custoSolucao = 0
    gv.tempoExecucaoInicial = datetime.datetime.now()
    while gv.totalEncomendas > 0:
        path_found = False
        if gv.totalEncomendas < N_ENCOMENDAS:
            encomenda_ronda = gv.totalEncomendas
        else:
            encomenda_ronda = N_ENCOMENDAS

        for i in range(0, encomenda_ronda + 1):
            source_node = matrix[source_coords[0], source_coords[1]]
            source_node.is_visited = True
            source_node.g = 0
            gv.nos_visitados.append(source_node)
            if i < encomenda_ronda:
                maiscurto = gv.encomendas_coord[0]
                maiscurto.g = 0
                for i in range(1, len(gv.encomendas_coord)):
                    gv.encomendas_coord[i].g = 0
                    if calculate_manhattan_distance(source_node,
                                                    maiscurto) + maiscurto.g > calculate_manhattan_distance(
                        source_node, gv.encomendas_coord[i]) + gv.encomendas_coord[i].g:
                        maiscurto = gv.encomendas_coord[i]
                destination_coords = maiscurto.coords
                encontrado = -1
                for co in range(len(gv.encomendas_coord)):
                    if gv.encomendas_coord[co].coords == maiscurto.coords: encontrado = co
                if encontrado >= 0:
                    gv.encomendas_coord.pop(encontrado)
                gv.totalEncomendas -= 1
            else:
                destination_coords = entrega_coords

            if not gv.pygame_started:
                init_pygame()
                return

            if path_found:
                # reset_last_grid()
                path_found = False

            if source_coords:

                # if gv.algo_selection.get() == 'Dijkstra':
                #     Dijkstra()
                #
                # if gv.algo_selection.get() == 'ASearch':
                #     ASearch()
                #
                # if gv.algo_selection.get() == 'BFS':
                #     BFS()
                #
                # if gv.algo_selection.get() == 'DFS':
                #     DFS()
                if gv.algo_selection == 'Dijkstra':
                    Dijkstra()

                if gv.algo_selection == 'ASearch':
                    ASearch()

                if gv.algo_selection == 'BFS':
                    BFS()

                if gv.algo_selection == 'DFS':
                    DFS()
    if gv.totalEncomendas == 0:
        gv.tempoExecucaoFinal = datetime.datetime.now()
        gv.tempoExecucao = gv.tempoExecucaoFinal - gv.tempoExecucaoInicial
        settings_win.t_estat.insert(END, "Número de nós visitados: " + str(gv.totalVisitados))
        settings_win.t_estat.insert(END,
                                    "\nTempo de execução de: " + str(gv.tempoExecucao.seconds) + " segundos e " + str(
                                        gv.tempoExecucao.microseconds) + " microsegundos")
        settings_win.t_estat.insert(END, "\nCusto da solução: " + str(gv.custoSolucao))
        save_stats()
        path_found = True


def set_contrast_mode():
    # global source_coords, destination_coords, matrix, pygame_started
    global source_coords, destination_coords, matrix

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

    if gv.pygame_started:
        reset_last_grid()


def check_for_events():
    """
    Listens for events inside of the pygame window
    """
    # global pygame_started, holding, screen
    global holding, screen

    for event in pygame.event.get():
        if event.type == QUIT:
            gv.pygame_started = False
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                gv.pygame_started = False
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
    if edit_mode_rb.get() == 5:
        current_mode = EDITING_MODES.ENTREGA


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
            if neighbour and neighbour.coords[0] == 10:
                print("dd")
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
            path_found = False
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
    if 0 <= x - 1:
        left_node = matrix[y][x - 1]

    right_node = None
    if x + 1 < WIDTH:
        right_node = matrix[y][x + 1]

    upper_node = None
    if 0 <= y - 1:
        upper_node = matrix[y - 1][x]

    lower_node = None
    if y + 1 < HEIGHT:
        lower_node = matrix[y + 1][x]

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

    gv.totalVisitados += 1
    node.is_visited = True
    gv.nos_visitados.append(node)
    # if gv.algo_selection.get() == 'Dijkstra':
    if gv.algo_selection == 'Dijkstra':
        if distance < node.distance_from_start:
            node.distance_from_start = distance
            node.predecessor = predecessor

    # if gv.algo_selection.get() == 'ASearch':
    if gv.algo_selection == 'ASearch':
        node.g = g
        node.h = h
        node.f = g + h
        node.predecessor = predecessor

    # if gv.algo_selection.get() == 'BFS':
    if gv.algo_selection == 'BFS':
        node.predecessor = predecessor

    # if gv.algo_selection.get() == 'DFS':
    if gv.algo_selection == 'DFS':
        node.predecessor = predecessor

    # if node.coords != destination_coords:

    if tuple(node.coords) != tuple(destination_coords):
        if not node.is_encomenda and not node.coords == entrega_coords:
            pygame.time.wait(gv.timeWait)
            rect = node.shape
            pygame.draw.rect(screen, VISITED, rect)
            pygame.display.update()
    else:
        path_found = True


# def highlight_path(neighbour: node.Node):
def highlight_path():
    """
    Highlights the path
    """
    global destination_coords, source_coords

    path_lenght = 0

    current = matrix[destination_coords[0], destination_coords[1]].predecessor
    # current = neighbour.predecessor
    # destino = neighbour
    caminho = []
    source_node = matrix[source_coords[0], source_coords[1]]
    caminho.clear()
    while current != source_node:
        caminho.append(current)
        current = current.predecessor

    for num in range(len(caminho) - 1, -1, -1):
        pygame.time.wait(gv.timeWait)
        rect = caminho[num].shape
        pygame.draw.rect(screen, PATH, rect)
        pygame.display.update()

    rect = source_node.shape
    if source_coords == entrega_coords:
        pygame.draw.rect(screen, ENTREGA, rect)
    else:
        pygame.draw.rect(screen, PATH, rect)

    source_node.is_wall = False

    for num in range(len(caminho) - 1, -1, -1):
        if num < len(caminho) - 1: rect = caminho[num + 1].shape
        gv.custoSolucao += 1
        pygame.draw.rect(screen, PATH, rect)
        source_coords = caminho[num].coords
        rect = caminho[num].shape
        pygame.draw.rect(screen, SOURCE, rect)
        pygame.display.update()
        pygame.time.wait(gv.timeWait)

    pygame.draw.rect(screen, PATH, rect)
    source_node = matrix[destination_coords[0], destination_coords[1]]
    source_node.is_visited = True
    source_node.is_encomenda = False
    source_coords = source_node.coords
    rect = matrix[destination_coords[0], destination_coords[1]].shape
    pygame.draw.rect(screen, SOURCE, rect)
    pygame.display.update()
    pygame.time.wait(gv.timeWait)
    limpar_visitados()
    print(path_lenght)


def limpar_visitados():
    for no in gv.nos_visitados:
        no.is_visited = False
        no.distance_from_start = np.inf
        no.g = np.inf
        no.h = np.inf
        no.f = np.inf
        if not no.is_encomenda:
            rect = no.shape
            pygame.draw.rect(screen, CELL, rect)
            pygame.display.update()

    gv.nos_visitados.clear()
    matrix[source_coords[0], source_coords[1]].distance_from_start = 0
    rect = matrix[source_coords[0], source_coords[1]].shape
    pygame.draw.rect(screen, SOURCE, rect)
    rect = matrix[entrega_coords[0], entrega_coords[1]].shape
    pygame.draw.rect(screen, ENTREGA, rect)
    pygame.display.update()


def main():
    init_settings_window()

    while running:
        root.update()

        if gv.pygame_started:
            check_for_events()

    root.destroy()


if __name__ == "__main__":
    main()
