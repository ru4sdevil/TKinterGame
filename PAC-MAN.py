import tkinter as tk
from tkinter import *
import random
import threading
import time

step = 30
colors = ['blue', 'green', 'yellow', 'red', 'orange', 'white']

master = tk.Tk()
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
N_Y = int(screen_height*0.8/step)
N_X = int(screen_width*0.8/step)



#===========================================================================
#Базовый класс двигающихся\анимированных обьектов
#===========================================================================
class Moving_object:

    def __init__(this, x = False, y = False):
        this.x, this.y = x,y

    def undraw(this):
        canvas.create_rectangle((this.x * step, this.y * step), ((this.x + 1) * step, (this.y + 1) * step), fill = 'black')
        

#===========================================================================
#Класс активного объекта
#===========================================================================
class Pac_Man(Moving_object):

    shut = True
    command = 0

    def __init__(this, x = False, y = False):
        super().__init__(x, y)

    def reset(this):
        this.shut = True
        this.command = 0
        this.undraw()
        this.x = 1
        this.y = N_Y - 2
        this.draw()

    def finished(this):
        if this.x >= N_X - 2 and this.y == 1:
            return True
        return False

    def tick(this):
        if this.finished():
            game.next_level()
        else:
            this.undraw()
            this.shut = not this.shut
            this.draw()

    def draw(this):
        if this.shut == True:
            canvas.create_image(this.x * step, this.y * step, anchor=NW, image = img_c[this.command])
        else:
            canvas.create_image(this.x * step, this.y * step, anchor=NW, image = img_o[this.command])


    def move(this, command):
        if command == 0:
            if maze.found_object(this.x + 1, this.y) == -1 and maze.cross(this.x + 1,this.y) == False and this.x + 1 < N_X:               
                this.undraw()
                this.x = this.x + 1
                this.command = 0
                this.draw()
            #right
        elif command == 1:
            if maze.found_object(this.x, this.y - 1) == -1 and maze.cross(this.x, this.y - 1) == False and this.y - 1 > 0:                
                this.undraw()
                this.y = this.y - 1
                this.command = 1
                this.draw()
            #up
        elif command == 2:
            if maze.found_object(this.x, this.y + 1) == -1 and maze.cross(this.x, this.y + 1) == False and this.y + 1 < N_Y:                
                this.undraw()
                this.y = this.y + 1
                this.command = 2
                this.draw()
            #down
        elif command == 3:
            if maze.found_object(this.x - 1, this.y) == -1 and maze.cross(this.x - 1,this.y) == False and this.x - 1 > 0:               
                this.undraw()
                this.x = this.x - 1
                this.command = 3
                this.draw()
            #left
        coins.check()
        frags.check()


#===========================================================================
#Классы призовых монет
#===========================================================================
class Coin(Moving_object):

    state = 0
    
    def __init__(this, x = False, y = False):
        super().__init__(x, y)
        this.draw()
        
    def draw(this):
        canvas.create_image(this.x * step, this.y * step, anchor=NW, image = img_coin[this.state])

    def tick(this):
        this.undraw()
        this.state += 1;
        if this.state > 3:
            this.state = 0
        this.draw()


class Coins:

    bank = []
    amount = 10

    def __init__(this):
        this.reset()

    def check(this):
        i = 0
        while i < len(this.bank):
            if pacman.x == this.bank[i].x and pacman.y == this.bank[i].y:
                this.bank[i].undraw()
                this.bank.pop(i)
                game.score += 1
                game.update()
            i += 1    
        

    def tick(this):
        for c in this.bank:
            c.tick()
        this.check()    
                

    
    def reset(this):
        i = 0
        this.bank.clear()
        while i < this.amount:
            x = random.randint(2, N_X - 3)
            y = random.randint(1, N_Y - 2)
            if maze.found_object(x,y) == -1:
                Coins.bank.append(Coin(x,y))
                i += 1
        
#===========================================================================
#Классы активных врагов
#===========================================================================
class Frag(Moving_object):

    state = 0
    
    def __init__(this, x = False, y = False):
        super().__init__(x, y)
        this.draw()
        
    def draw(this):
        canvas.create_image(this.x * step, this.y * step, anchor=NW, image = img_frag[this.state])

    def try_move(this):
        x = random.randint(-1, 1)
        if x == 0:
            y = random.randint(-1, 1)
        else:
            y = 0
        x = this.x + x
        y = this.y + y     
        if maze.found_object(x,y) == -1 and maze.cross(x,y) == False:
            this.x = x
            this.y = y
        

    def tick(this):
        this.undraw()
        this.try_move()
        this.state += 1;
        if this.state > 3:
            this.state = 0
        this.draw()


class Frags:

    zoo = []
    amount = 10

    def __init__(this):
        this.reset()

    def check(this):
        i = 0
        while i < len(Frags.zoo):
            if pacman.x == Frags.zoo[i].x and pacman.y == Frags.zoo[i].y:
                game.over()
            i += 1    
        

    def tick(this):
        for f in this.zoo:
            f.tick()
        this.check()    
                

    
    def reset(this):
        i = 0
        this.zoo.clear()
        while i < this.amount:
            x = random.randint(2, N_X - 3)
            y = random.randint(1, N_Y - 2)
            if maze.found_object(x,y) == -1:
                Frags.zoo.append(Frag(x,y))
                i += 1


#===========================================================================
#Основной геймплей
#===========================================================================
class Game:

    started = False
    blocked = True
    level = 1
    score = 0
    

    def __init__(this):
        pass

    def welcome(this):
        this.blocked = True
        canvas.update()
        canvas.create_rectangle( (int(N_X * step / 8*3), int(N_Y * step / 8*3) ), (int(N_X * step / 8*5), int(N_Y * step / 8*5) ), fill = 'black', outline = 'green')
        t = canvas.create_text(int(N_X * step / 2), int(N_Y * step / 2), fill='green', font='Arial 20', width=int(N_X * step / 8*2),text = 'Press Enter to start')
        print(canvas.bbox(t))
        

    def update(this):
        maze.n_wall.draw()
        t = canvas.create_text(int(N_X * step / 2), 0, fill='yellow', font='Arial 20', anchor = NE, text = f'Level: {this.level} ')
        print(canvas.bbox(t))
        t = canvas.create_text(int(N_X * step / 2), 0, fill='yellow', font='Arial 20', anchor = NW, text = f'Score: {this.score} ')
        print(canvas.bbox(t))

    def over(this):
        this.started = False
        this.blocked = True
        pacman.undraw()
        canvas.create_rectangle( (int(N_X * step / 8*3), int(N_Y * step / 8*3) ), (int(N_X * step / 8*5), int(N_Y * step / 8*5) ), fill = 'black', outline = 'red')
        t = canvas.create_text(int(N_X * step / 2), int(N_Y * step / 2), fill='red', font='Arial 32', width=int(N_X * step / 8*2),text = 'Game Over!')
        print(canvas.bbox(t))

        this.level = 1
        this.score = 0
        coins.amount = 10
        frags.amount = 10
        
          
    def setup_level(this):
        canvas.create_rectangle((0,0), (N_X * step, N_Y * step), fill = 'black') 
        maze.reset()
        pacman.reset()
        coins.reset()
        frags.reset()
        this.update()

    
    def next_level(this):
        this.started = False
        this.level += 1
        coins.amount += 2
        frags.amount += 2
        this.welcome()
    
    def timer(this):
        if not this.blocked:
            if this.started:
                coins.tick()
                frags.tick()
                pacman.tick()                
          

    def key_listener(this,key):

        if this.blocked:
            this.blocked = False
            this.setup_level()

        if key == 13:
            if not this.started:
                this.started = True

        if this.started: 
            if key == 27:
                if this.started:
                    this.started = False
            
            
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

 
        
#===========================================================================
#Базовый класс статических стен 
#===========================================================================
class Wall:
    
    def __init__(this, x_1 = False, y_1 = False, x_2 = False, y_2 = False, color = 'blue'):
        this.x_1, this.y_1 = x_1, y_1
        this.x_2, this.y_2 = x_2, y_2
        this.color = color

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


        
#===========================================================================
#Классы случайных стен (препятствий)
#===========================================================================
class Random_wall:
   
    def __init__(this, x = False, y = False, color = 'blue'):
        this.x, this.y = x,y
        this.color = colors[random.randint(0, 5)]
        
    def draw(this):
        canvas.create_rectangle((this.x * step, this.y * step), ((this.x + 1) * step, (this.y + 1) * step), fill = this.color)
    


class Maze:

    density = 0.3

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

    def reset(this):
        this.objects.clear()
        for i in range(int(N_X * N_Y * this.density)):
            x = random.randint(2, N_X - 3)
            y = random.randint(1, N_Y - 2)
            if this.found_object(x,y) == -1:
               Maze.objects.append(Random_wall(x, y))
        
        this.checking()        
        
        for object_i in Maze.objects:
            object_i.draw()

        this.n_wall.draw()
        this.s_wall.draw()
        this.e_wall.draw()
        this.w_wall.draw()
    
        
    def __init__(this):
        this.reset()


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

#===========================================================================
#Обработчик нажатий клавиатуры
#===========================================================================
def keypress(event):
    keys = {37,38,39,40,65,68,87,13,27}
    if event.keycode in keys:
        game.key_listener(event.keycode)

#===========================================================================
#Вспомогательный класс интервальных событий
#===========================================================================
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

#===========================================================================
#Основной код программы
#===========================================================================

canvas = tk.Canvas(master, bg='black', height = step*N_Y, width = step*N_X)

img_c = []
img_c.append(PhotoImage(file="..\TKinterGame\close_r.gif"))
img_c.append(PhotoImage(file="..\TKinterGame\close_u.gif"))
img_c.append(PhotoImage(file="..\TKinterGame\close_d.gif"))
img_c.append(PhotoImage(file="..\TKinterGame\close_l.gif"))

img_o = []
img_o.append(PhotoImage(file="..\TKinterGame\open_r.gif"))
img_o.append(PhotoImage(file="..\TKinterGame\open_u.gif"))
img_o.append(PhotoImage(file="..\TKinterGame\open_d.gif"))
img_o.append(PhotoImage(file="..\TKinterGame\open_l.gif"))


img_coin = []
img_coin.append(PhotoImage(file="..\TKinterGame\coin_r.gif"))
img_coin.append(PhotoImage(file="..\TKinterGame\coin_d.gif"))
img_coin.append(PhotoImage(file="..\TKinterGame\coin_l.gif"))
img_coin.append(PhotoImage(file="..\TKinterGame\coin_u.gif"))

img_frag = []
img_frag.append(PhotoImage(file="..\TKinterGame\omg_r.gif"))
img_frag.append(PhotoImage(file="..\TKinterGame\omg_d.gif"))
img_frag.append(PhotoImage(file="..\TKinterGame\omg_l.gif"))
img_frag.append(PhotoImage(file="..\TKinterGame\omg_u.gif"))


        
maze = Maze()
pacman = Pac_Man(1, N_Y - 2)
pacman.draw()
game = Game()
coins = Coins()
frags = Frags()

game.update()
game.welcome()

master.bind('<KeyPress>', keypress)

timer = IntervalTimer(0.5,timerevent)
timer.start()

canvas.pack()
master.mainloop()
timer.stop()
