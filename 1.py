import tkinter as tk
import random

class Player:

    objects = {(-1,-1)}

    def __init__(this, color):
        this.x, this.y = -1,-1
        while (this.x, this.y) in Player.objects:
            this.x = this.random_pos(N_X)
            this.y = this.random_pos(N_Y)
        Player.objects.add((this.x, this.y))
        this.color = color
        this.draw()

    def draw(this):
        this.body = canvas.create_oval((this.x, this.y), (this.x+step, this.y+step), fill = this.color)
        
    def random_pos(this, top):
        return random.randint(1, top-1)*step

    def repaint(this, x, y):
        old_x,old_y = this.x,this.y
        this.x =(this.x+x)%(step*N_X)
        this.y =(this.y+y)%(step*N_Y)
        canvas.move(this.body, (this.x- old_x), (this.y - old_y))

class Exit(Player):
    def __init__(this):
        super().__init__("yellow")

class Enemy(Player):
    def __init__(this, color='red'):
        super().__init__(color)

class EnemyD(Enemy):
    
    def __init__(this):
        super().__init__('orange')
        
    def random_step(this):
        p = random.randint(1,4)
        if p == 1:
            super().repaint(0, -step)
            #up
        elif p == 2:
            super().repaint(0, step)
            #down
        elif p == 3:
            super().repaint(-step, 0)
            #left
        elif p == 4:
            super().repaint(step, 0)
            #right

class Hero(Player):
    def __init__(this):
        super().__init__('green')
        
    def check_pos(this, other):
        return ((this.x == other.x) and (this.y == other.y))
    
def keypress(event):
    
    print(event)
    keys = {37,38,39,40,65,68,87}
    if event.keycode in keys:
        key_listener(event.keycode)
        enemies_step()
        endgame()

def key_listener(key):
    
    if key == 38 or key == 87:
        player.repaint(0, - step)
        #up
            
    elif key == 39 or key == 68:
        player.repaint(step, 0)
        #right
            
    elif key == 37 or key == 65:
        player.repaint(- step, 0)
        #left
            
    elif key == 40 or key == 83:
        player.repaint(0, step)
        #down

def enemies_step():
    for enemy in enemies_d:
        enemy.random_step()

def endgame():
    if player.check_pos(exit_q):
        print('GAME OVER')
        print('YOU WON!!!')
    enemies = enemies_d+enemies_s
    for enemy in enemies:
        if player.check_pos(enemy):
            print('GAME OVER')
            print('YOU LOSE!!!')
            break

def add_enemies():
    for i in range(6):
        enemy = Enemy()
        enemies_s.append(enemy)
    for i in range(3):
        enemy = EnemyD()
        enemies_d.append(enemy)

master = tk.Tk()
step = 60
N_X = 11
N_Y = 11
enemies_s = []
enemies_d = []
canvas = tk.Canvas(master, bg='blue', height = step*N_X, width = step*N_Y)

add_enemies()
player = Hero()
exit_q = Exit()
canvas.pack()
master.bind('<KeyPress>', keypress)
master.mainloop()
