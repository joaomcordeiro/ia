import os
import platform
import pygame
import tkinter as tk
from logging import root
from tkinter import *
from tkinter.ttk import Combobox
from test import *

from cl_enum import Enum


class TkWindow:
    """
    Class used to handle the tkinter window
    """

    def __init__(self, win):
        global algo_selection, edit_mode_rb, high_contrast_mode

        #####   DECLARING LABELS AND ENTRIES   #####
        self.lbl_rows = Label(win, text='Rows:')
        self.lbl_cols = Label(win, text='Columns:')
        self.lbl_cell_size = Label(win, text='Cell Size:')
        self.lbl_algo = Label(win, text='Algorithm:')
        self.t_rows = Entry()
        self.t_rows.insert(END, str(ROWS))
        self.t_cols = Entry()
        self.t_cols.insert(END, str(COLUMNS))
        self.t_cell_size = Entry()
        self.t_cell_size.insert(END, str(CELL_SIZE))

        algo_selection.set('Dijkstra')
        data = ('Dijkstra', 'ASearch', 'BFS', 'DFS')
        self.cb = Combobox(win, values=data)
        self.cb.bind('<<ComboboxSelected>>', self.change_algo_selection)
        self.cb.current(0)

        #####   RADIO BUTTONS    #####
        edit_mode_rb.set(1)
        self.lbl_editmode = Label(win, text='Editing Mode:')
        self.rb_src = Radiobutton(
            win, text='Source', variable=edit_mode_rb, value=1, command=change_editing_mode)
        self.rb_dest = Radiobutton(
            win, text='Destination', variable=edit_mode_rb, value=2, command=change_editing_mode)
        self.rb_wall = Radiobutton(
            win, text='Wall', variable=edit_mode_rb, value=3, command=change_editing_mode)
        self.rb_erase = Radiobutton(
            win, text='Erase', variable=edit_mode_rb, value=4, command=change_editing_mode)

        high_contrast_mode.set(False)
        self.cb_contrast_mode = Checkbutton(
            win, text="High Contrast", variable=high_contrast_mode, command=set_contrast_mode)

        #####   BUTTONS    #####
        self.btn_find = Button(win, text='Find Path', command=find_path)
        self.btn_build_grid = Button(
            win, text='Build Grid', command=self.build_click)
        self.btn_reset_last_grid = Button(
            win, text='Reset Last', command=reset_last_grid)

        self.btn_load_grid = Button(win, text='Load Grid', command=load_grid)
        self.btn_save_grid = Button(win, text='Save Grid', command=save_grid)
        #####   PLACING #####

        self.lbl_rows.place(x=50, y=40)
        self.t_rows.place(x=150, y=40)
        self.lbl_cols.place(x=50, y=80)
        self.t_cols.place(x=150, y=80)
        self.lbl_cell_size.place(x=50, y=120)
        self.t_cell_size.place(x=150, y=120)
        self.lbl_algo.place(x=50, y=160)

        self.cb.place(x=150, y=160)

        self.lbl_editmode.place(x=50, y=200)
        self.rb_src.place(x=150, y=200)
        self.rb_dest.place(x=150, y=220)
        self.rb_wall.place(x=150, y=240)
        self.rb_erase.place(x=150, y=260)

        self.btn_build_grid.place(x=50, y=300)
        self.btn_reset_last_grid.place(x=150, y=300)
        self.btn_find.place(x=250, y=340)
        self.btn_load_grid.place(x=50, y=340)
        self.btn_save_grid.place(x=150, y=340)

        self.cb_contrast_mode.place(x=230, y=300)

        root.title('Pathfinder Settings')
        root.geometry("350x400+10+10")

        os.environ['SDL_WINDOWID'] = str(root.winfo_id())
        if platform.system == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'

        os.environ['SDL_VIDEO_CENTERED'] = '0'

    def build_click(self):
        tmp_rows = int(self.t_rows.get())
        tmp_cols = int(self.t_cols.get())
        tmp_cell_size = int(self.t_cell_size.get())

        refresh_rows_cols(tmp_rows, tmp_cols, tmp_cell_size)
        init_pygame()

    def change_algo_selection(self, event):
        global algo_selection
        algo_selection.set(self.cb.get())


def close():
    """
    Closes the program
    """
    global running, pygame_started
    running = False
    pygame_started = False
    pygame.quit()
