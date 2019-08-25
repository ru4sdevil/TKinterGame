import tkinter as tk
import random

step = 30
N_X = 33
N_Y = 11

colors = ['blue', 'green', 'yellow', 'red', 'orange', 'white']




master = tk.Tk()
canvas = tk.Canvas(master, bg='black', height = step*N_Y, width = step*N_X)

class Wall:

    
    def __init__(this, x_1 = False, y_1 = False, x_2 = False, y_2 = False, color = 'blue'):
        this.x_1, this.y_1 = x_1, y_1
        this.x_2, this.y_2 = x_2, y_2
        this.color = color
        this.draw()

    def cross(this, x = 0, y = 0):
        print(x, y, this.x_1,this.y_1,this.x_2,this.y_2)
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
        this.body = canvas.create_rectangle((this.x * step, this.y * step), ((this.x + 1) * step, (this.y + 1) * step), fill = this.color)
    


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
        print('try',x,y)
        if this.cross(x,y) == False:
            pos = this.found_object(x,y)
            if pos != -1:
                Maze.objects.pop(pos)
                print('del =',x,y)
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
        for i in range(100):
            x = random.randint(2, N_X - 3)
            y = random.randint(1, N_Y - 2)
            Maze.objects.append(Random_wall(x, y))
        
        this.sort()
#        this.unique()
#        for object_i in Maze.objects:
 #           object_i.draw()

        this.checking()        
        
        for object_i in Maze.objects:
            object_i.draw()

        print('length =',len(Maze.objects))


    def sort(this):
        for object_l in Maze.objects:
            for object_r in Maze.objects:
                if object_l.x < object_r.x:
                    object_l.x, object_r.x = object_r.x, object_l.x
                    object_l.y, object_r.y = object_r.y, object_l.y
                    object_l.color, object_r.color = object_r.color, object_l.color
                elif object_l.x == object_r.x:
                    if object_l.y < object_r.y:
                        object_l.x, object_r.x = object_r.x, object_l.x
                        object_l.y, object_r.y = object_r.y, object_l.y
                        object_l.color, object_r.color = object_r.color, object_l.color
        for object_l in Maze.objects:
            print(object_l.x,object_l.y)

    def unique(this):
        for i in range(1, len(Maze.objects)):
            if Maze.objects[i].x == Maze.objects[i-1].x and Maze.objects[i].y == Maze.objects[i-1].y:
                Maze.objects.pop(i)
            

    def checking(this):
        t_x = 1
        t_y = N_Y - 2
        s = 0
        while s < 50:
            print('check iter =',s,t_x,t_y)    
            canvas.create_rectangle((t_x * step + 10, t_y * step + 10), ((t_x + 1) * step - 10, (t_y + 1) * step - 10), fill = 'teal')
            s += 1
            if this.found_object(t_x + 1, t_y) == -1:
                if this.cross(t_x + 1,t_y) == False:
                    t_x = t_x + 1
                    continue
            elif this.found_object(t_x, t_y + 1) == -1:
                if this.cross(t_x,t_y + 1) == False:
                    t_y = t_y + 1
                    continue
            elif this.found_object(t_x, t_y - 1) == -1:
                if this.cross(t_x,t_y - 1) == False:
                    t_y = t_y - 1
                    continue
            print('chectry',t_x,t_y)    
            if this.try_break(t_x +1, t_y) == True:
                t_x = t_x + 1
                continue
            elif this.try_break(t_x, t_y + 1) == True:
                t_y = t_y + 1
                continue
            elif this.try_break(t_x, t_y - 1) == True:
                t_y = t_y - 1
                continue
        
#            if t_x == N_X - 1 and t_y == 1:
##                break
        
maze = Maze()

canvas.pack()
master.mainloop()
