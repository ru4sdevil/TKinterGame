import tkinter as tk
import random

def random_pos(top):
    return random.randint(1, top-1)*step

class Player:

    def __init__(this, color):
        this.x = random_pos(N_X)
        this.y = random_pos(N_Y)
        this.color = color

    def draw(this):
        canvas.create_oval((this.x, this.y), (this.x+step, this.y+step), fill = this.color)
        
    def random_pos(top):
        return random.randint(1, top-1)*step

master = tk.Tk()
step = 60
N_X = 10
N_Y = 10
canvas = tk.Canvas(master, bg='blue', height = step*N_X, width = step*N_Y)

player = Player('green')
player.draw()
exit_q = Player('red')
exit_q.draw()
canvas.pack()
master.mainloop()
