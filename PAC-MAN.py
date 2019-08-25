import tkinter as tk
##import random

step = 30
N_X = 33
N_Y = 11


master = tk.Tk()
canvas = tk.Canvas(master, bg='black', height = step*N_Y, width = step*N_X)

class Wall:

    def __init__(this, x_1 = False, y_1 = False, x_2 = False, y_2 = False, color = 'blue'):
        this.x_1, this.y_1 = x_1, y_1
        this.x_2, this.y_2 = x_2, y_2
        this.color = color
        this.draw()

    def draw(this):
       this.wall = canvas.create_rectangle((this.x_1, this.y_1), (this.x_2, this.y_2), fill = this.color, outline = this.color) 

class N_wall(Wall):
    def __init__(this, x_1 = 0, y_1 = 0, x_2 = step * N_X, y_2 = step):
        super().__init__(x_1, y_1, x_2, y_2)

class S_wall(Wall):
    def __init__(this, x_1 = 0, y_1 = step * (N_Y - 1), x_2 = step * N_X, y_2 = step * N_Y):
        super().__init__(x_1, y_1, x_2, y_2)

class E_wall(Wall):
    def __init__(this, x_1 = 0, y_1 = 0, x_2 = step * 2, y_2 = step * (N_Y - 2)):
        super().__init__(x_1, y_1, x_2, y_2)

class W_wall(Wall):
    def __init__(this, x_1 = step * (N_X - 2), y_1 = step * 2, x_2 = step * N_X, y_2 = step * N_Y):
        super().__init__(x_1, y_1, x_2, y_2)
        
n_wall = N_wall()
s_wall = S_wall()
e_wall = E_wall()
w_wall = W_wall()

canvas.pack()
master.mainloop()

