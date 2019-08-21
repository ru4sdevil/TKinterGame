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
        this.body = canvas.create_oval((this.x, this.y), (this.x+step, this.y+step), fill = this.color)
        
    def random_pos(top):
        return random.randint(1, top-1)*step

    def repaint(this, x, y):
        canvas.move(this.body, x, y)

    def check_pos(this, other):
        return ((this.x == other.x) and (this.y == other.y))
        
        
def keypress(event):
    
    print(event)
    
    if event.keycode == 38 or event.keycode == 87:
        player.y -= step
        player.repaint(0, - step)
        #up
        
    elif event.keycode == 39 or event.keycode == 68:
        player.x += step
        player.repaint(step, 0)
        #right
        
    elif event.keycode == 37 or event.keycode == 65:
        player.x -= step
        player.repaint(- step, 0)
        #left
        
    elif event.keycode == 40 or event.keycode == 83:
        player.y += step
        player.repaint(0, step)
        #down
    endgame()

def endgame():
    if player.check_pos(exit_q):
        print('GAME OVER')
        print('YOU WON!!!')
        
master = tk.Tk()
step = 60
N_X = 10
N_Y = 10
canvas = tk.Canvas(master, bg='blue', height = step*N_X, width = step*N_Y)

player = Player('green')
player.draw()
exit_q = Player('yellow')
exit_q.draw()
canvas.pack()
master.bind('<KeyPress>', keypress)
master.mainloop()
