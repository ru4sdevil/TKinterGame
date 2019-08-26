import tkinter as tk
from tkinter import *
import random
import threading

step = 30
colors = ['blue', 'green', 'yellow', 'red', 'orange', 'white']

density = 0.3


master = tk.Tk()

screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()

N_Y = int(screen_height*0.8/step)
N_X = int(screen_width*0.8/step)


global img_c,img_o

canvas = tk.Canvas(master, bg='black', height = step*N_Y, width = step*N_X)

class Moving_object:

    def __init__(this, x = False, y = False):
        this.x, this.y = x,y

class Pac_Man(Moving_object):

    shut = False

    def __init__(this, x = False, y = False):
        super().__init__(x, y)

    def tick(this):
        this.undraw()
        this.shut = not this.shut
        this.draw()


    def draw(this):
        if this.shut == True:
            canvas.create_image(this.x * step, this.y * step, anchor=NW, image=img_c)
        else:
            canvas.create_image(this.x * step, this.y * step, anchor=NW, image=img_o)

            
    def undraw(this):
        canvas.create_rectangle((this.x * step, this.y * step), ((this.x + 1) * step, (this.y + 1) * step), fill = 'black')

    def move(this, command):
        print(f'command = {command}')
        if command == 0:
            if maze.found_object(this.x + 1, this.y) == -1 and maze.cross(this.x + 1,this.y) == False:               
                this.undraw()
                this.x = this.x + 1
                this.draw()
            #right
        elif command == 1:
            if maze.found_object(this.x, this.y - 1) == -1 and maze.cross(this.x, this.y - 1) == False:                
                this.undraw()
                this.y = this.y - 1
                this.draw()
            #up
        elif command == 2:
            if maze.found_object(this.x, this.y + 1) == -1 and maze.cross(this.x, this.y + 1) == False:                
                this.undraw()
                this.y = this.y + 1
                this.draw()
            #down
        elif command == 3:
            if maze.found_object(this.x - 1, this.y) == -1 and maze.cross(this.x - 1,this.y) == False:               
                this.undraw()
                this.x = this.x - 1
                this.draw()
            #left

    
class Game:

    def __init__(this):
         pass

    def timer(this):
        pass

    def key_listener(this,key):
        
        if key == 38 or key == 87:
            pacman.move(1)
            #up
                
        if key == 39 or key == 68:
            pacman.move(0)
            #right
                
        if key == 37 or key == 65:
            pacman.move(3)
            #left
                
        if key == 40 or key == 83:
            pacman.move(2)
            #ascii

 
        

class Wall:
    
    def __init__(this, x_1 = False, y_1 = False, x_2 = False, y_2 = False, color = 'blue'):
        this.x_1, this.y_1 = x_1, y_1
        this.x_2, this.y_2 = x_2, y_2
        this.color = color
        this.draw()

    def cross(this, x = 0, y = 0):
        if x >= this.x_1 and x < this.x_2 and y >= this.y_1 and y < this.y_2:
            return True
        return False

    def draw(this):
       this.wall = canvas.create_rectangle((this.x_1 * step, this.y_1 * step), (this.x_2 * step, this.y_2 * step), fill = this.color, outline = this.color) 



class N_wall(Wall):
    def __init__(this, x_1 = 0, y_1 = 0, x_2 = N_X, y_2 = 1):
        super().__init__(x_1, y_1, x_2, y_2)

class S_wall(Wall):
    def __init__(this, x_1 = 0, y_1 = (N_Y - 1), x_2 = N_X, y_2 = N_Y):
        super().__init__(x_1, y_1, x_2, y_2)

class E_wall(Wall):
    def __init__(this, x_1 = 0, y_1 = 0, x_2 = 2, y_2 = N_Y - 2):
        super().__init__(x_1, y_1, x_2, y_2)

class W_wall(Wall):
    def __init__(this, x_1 = N_X - 2, y_1 = 2, x_2 = N_X, y_2 = N_Y):
        super().__init__(x_1, y_1, x_2, y_2)


        

class Random_wall:
   
    def __init__(this, x = False, y = False, color = 'blue'):
        this.x, this.y = x,y
        this.color = colors[random.randint(0, 5)]
        
    def draw(this):
        canvas.create_rectangle((this.x * step, this.y * step), ((this.x + 1) * step, (this.y + 1) * step), fill = this.color)
    


class Maze:

    objects = []
    n_wall = N_wall()
    s_wall = S_wall()
    e_wall = E_wall()
    w_wall = W_wall()

    def found_object(this, x = 0, y = 0):
        for i in range(len(Maze.objects)):
            if Maze.objects[i].x == x and Maze.objects[i].y == y:
                return i
        return -1

    def try_break(this, x = 0, y = 0):
        if this.cross(x,y) == False:
            pos = this.found_object(x,y)
            if pos != -1:
                Maze.objects.pop(pos)
                return True
        return False

    def cross(this, x = 0, y = 0):
        if this.n_wall.cross(x,y) == True:
            return True
        elif this.s_wall.cross(x,y) == True:
            return True
        elif this.e_wall.cross(x,y) == True:
            return True
        elif this.w_wall.cross(x,y) == True:
            return True
        return False

        
        
    def __init__(this):
        for i in range(int(N_X * N_Y * density)):
            x = random.randint(2, N_X - 3)
            y = random.randint(1, N_Y - 2)
            Maze.objects.append(Random_wall(x, y))
        
        Maze.objects.sort(key=lambda Random_wall: Random_wall.x+Random_wall.y*N_X )
           
        this.unique()

        this.checking()        
        
        for object_i in Maze.objects:
#            print(object_i.x,object_i.y)
            object_i.draw()

        print('length =',len(Maze.objects))


    def unique(this):
        w_x = -1
        w_y = -1
        i = 0
        while i < len(Maze.objects):
            if Maze.objects[i].x == w_x and Maze.objects[i].y == w_y:
                Maze.objects.pop(i)
            else:
                w_x = Maze.objects[i].x
                w_y = Maze.objects[i].y
                i += 1
            

    def checking(this):
        t_x = 1
        t_y = N_Y - 2
        p_x = 0
        p_y = t_y
        s = 0
        while s < (N_X*N_Y/2):
            if t_x == N_X - 2 and t_y == 1:
                break
            s += 1
            
            if this.found_object(t_x + 1, t_y) == -1 and this.cross(t_x + 1,t_y) == False and t_x + 1 != p_x:
                p_x = t_x
                p_y = t_y                
                t_x = t_x + 1
                continue
            if this.found_object(t_x, t_y - 1) == -1 and this.cross(t_x,t_y - 1) == False and t_y - 1 != p_y:
                p_x = t_x
                p_y = t_y                
                t_y = t_y - 1
                continue
            if this.found_object(t_x, t_y + 1) == -1 and this.cross(t_x,t_y + 1) == False and t_y + 1 != p_y and t_x <= this.e_wall.x_1:
                p_x = t_x
                p_y = t_y                
                t_y = t_y + 1
                continue
#            if this.found_object(t_x-1, t_y) == -1 and this.cross(t_x-1,t_y) == False and t_x - 1 != p_x:
 #               p_x = t_x
  #              p_y = t_y                
   #             t_x = t_x - 1
    #            continue
            elif this.try_break(t_x +1, t_y) == True:
                p_x = t_x
                p_y = t_y                
                t_x = t_x + 1
                continue
            elif this.try_break(t_x, t_y - 1) == True:
                p_x = t_x
                p_y = t_y
                t_y = t_y - 1
                continue
            elif this.try_break(t_x, t_y + 1) == True:
                p_x = t_x
                p_y = t_y
                t_y = t_y + 1
                continue
        print('end iter =',s)


def keypress(event):
    print(event)
    keys = {37,38,39,40,65,68,87}
    if event.keycode in keys:
        game.key_listener(event.keycode)


class IntervalTimer():
    def __init__(self,I,hFunc):
        self.I = I
        self.hFunc = hFunc
        self.thread = threading.Timer(self.I,self.handle_func)

    def handle_func(self):
        self.hFunc()
        self.thread = threading.Timer(self.I,self.handle_func)
        self.thread.start()

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.cancel()
        self.thread.join()    

def timerevent():
    game.timer()
    pacman.tick()


img_c = PhotoImage(file="..\TKinterGame\pacman_c.gif")
img_o = PhotoImage(file="..\TKinterGame\pacman_o.gif")
        
maze = Maze()
pacman = Pac_Man(1, N_Y - 2)
pacman.draw()
game = Game()

master.bind('<KeyPress>', keypress)

timer = IntervalTimer(0.5,timerevent)
timer.start()

canvas.pack()
master.mainloop()
timer.stop()

