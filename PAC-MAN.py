import tkinter as tk
##import random

step = 30
N_X = 33
N_Y = 11
master = tk.Tk()
canvas = tk.Canvas(master, bg='black', height = step*N_Y, width = step*N_X)

class Wall():
    def __init__(this, x, y, color = 'blue'):
        this.x = x
        this.y = y
        this.color = color
        this.outline = color
        this.draw()

    def draw(this):
        this.body = canvas.create_rectangle((this.x, this.y), fill = this.color, outline = this.outline)
        
wall = Wall()

canvas.pack()
master.mainloop()
