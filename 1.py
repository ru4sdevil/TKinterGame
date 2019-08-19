import tkinter as tk
import random

def random_pos(top):
    return random.randint(1, top-1)*step

master = tk.Tk()
step = 60
N_X = 10
N_Y = 10
canvas = tk.Canvas(master, bg='blue', height = step*N_X, width = step*N_Y)



player_pos = (random_pos(N_X),  random_pos(N_Y))
exit_pos = (random_pos(N_X), random_pos(N_Y))
