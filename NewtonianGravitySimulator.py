from operator import truediv
import pygame
import copy
from pygame import gfxdraw
import random
#import pygame_widgets
#import StackoverflowSlider

#from pygame_widgets.slider import Slider
#from pygame_widgets.textbox import TextBox
import math



""" !!!!!!!!!!!!!!   WISHLIST   !!!!!!!!!!!!!!!!
    1) Object Trails                 DONE
    2) Add objects with mouse events DONE
    3) Slider for time
    4) Reverse time?????
    5) Collisions
    6)
"""


# Color Constants
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GRAY =  (200, 200, 200)
BLUE = (0,   0,   255)
GREEN = (0,   255, 0)
RED = (255, 0,   0)
YELLOW = (255,   255, 0)

# Speed and Gravitational Constant
dt = 0.1
G = 1

# Size of
HEIGHT = 600
WIDTH = 1000


class Asteroid:
    def __init__(self, x, dx, y, dy, m, r, color):
        self.x = x
        self.dx = dx
        self.y = y
        self.dy = dy
        self.m = m
        self.r = r
        self.color = color

class AsteroidTrail:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        





AST0 = Asteroid(WIDTH / 2 - 200, 0, HEIGHT / 2, 10, 10,
                4, WHITE)
AST1 = Asteroid(WIDTH / 2, 0, HEIGHT / 2, 0, 1000,
                10, YELLOW)
AST2 = Asteroid(WIDTH / 2 + 200, 0, HEIGHT / 2, -10, 10,
                4, WHITE)

STABLETWOBODYORBIT = [Asteroid(WIDTH / 2 - 200, -1, HEIGHT / 2, 10, 10,
                               4, WHITE),
                      Asteroid(WIDTH / 2, 0, HEIGHT / 2, -0.1, 1000,
                               10, YELLOW)]

THREEBODYORBIT = [Asteroid(WIDTH / 2 - 200, 0, HEIGHT / 2, 11 , 3000,
                           6, RED),
                  Asteroid(WIDTH / 2, 0, HEIGHT / 2, 0, 3000,
                           10, YELLOW),
                  Asteroid(WIDTH / 2 + 200, 0, HEIGHT / 2, 20, 10000,
                           4, WHITE)]

TWOOBJECTSPINORBIT = [Asteroid(WIDTH / 2 - 75, 0, HEIGHT / 2, 2, 10000,
                               5, BLUE),
                      Asteroid(WIDTH / 2 + 75, 0, HEIGHT / 2, -2, 10000,
                               5, YELLOW)]

COLLISION = [Asteroid(WIDTH / 2 + 200, -2, HEIGHT / 2, 0, 100,
                               10, WHITE),
                      Asteroid(WIDTH / 2 - 200, 7, HEIGHT / 2, 0, 10,
                               10, YELLOW)]

BLACKHOLE = [Asteroid(WIDTH / 2, 0, HEIGHT / 2, 0, 20000,
                               10, WHITE)]

STARTCOND = copy.deepcopy(TWOOBJECTSPINORBIT)


def nextasteroid(a):
    a.x = a.x + dt * a.dx
    a.y = a.y + dt * a.dy
    return a


def dist(one, two):
    return math.hypot((one.x - two.x), (one.y - two.y))


def nextasteroids(loa, lot, trails):
    oldloa = loa
    listout = []
    #ke=0
    #pe=0
    px=0
    py=0

    # Iterating upon old values to find new values
    for a in loa:
        for old in oldloa:
            # Not objects on themselves(would be dividing by 0)
            hypotenuse = (math.hypot(abs(a.x - old.x), abs(a.y - old.y)))
            if (a.x == old.x and a.y == old.y):
                accel = 0
                theta = 0
            else:
                if (hypotenuse < a.r):
                    hypotenuse = a.r / 2
                accel = (G * old.m) / (hypotenuse ** 2)
                theta = math.atan2((a.x - old.x), (a.y - old.y))
                #pe = pe + G * a.m * old.m / (math.hypot(abs(a.x - old.x), abs(a.y - old.y)))
                


            ax = accel * math.sin(theta)
            ay = accel * math.cos(theta)

            a.dx = a.dx - ax * dt
            a.dy = a.dy - ay * dt
        listout.append(a)
            
        #ke= ke + (1/2) * a.m * (a.dx**2+a.dy**2) 
        
    
    #print(ke)
    #print(pe)
    #print(ke + pe)
    #print("---------------------")


    
    #Stepping forward position with velocity 
    temp = listout
    for a in listout:
        for b in temp:
            if colliding(a, b) and not (a == b):
                if a.m > b.m:
                    a.dx = (a.m * a.dx + b.m * b.dx)/ (a.m+b.m)
                    a.dy = (a.m * a.dy + b.m * b.dy)/ (a.m+b.m)
                    a.m += b.m
                    a.r = round(math.sqrt(a.r**2 + b.r**2))
                    listout.remove(b)
                else:
                    b.dx = (a.m * a.dx + b.m * b.dx)/ (a.m+b.m)
                    b.dy = (a.m * a.dy + b.m * b.dy)/ (a.m+b.m)
                    b.m += a.m
                    b.r = round(math.sqrt(a.r**2 + b.r**2))
                    listout.remove(a)
        a = nextasteroid(a)

        if trails:
            lot.append(AsteroidTrail(int(a.x), int(a.y), a.color))
        if abs(a.x) > 10000 or abs(a.y) > 10000:
            listout.remove(a)
    return (listout, lot)

def colliding(a1, a2):
    return not bool(a1.r + a2.r < abs(math.hypot(abs(a1.x - a2.x), abs(a1.y - a2.y))))


def drawasteroid(screen, a):
    gfxdraw.aacircle(screen, int(a.x), int(a.y), a.r, a.color)
    gfxdraw.filled_circle(screen, int(a.x), int(a.y), a.r, a.color)


def drawasteroids(screen, loa):
    for a in loa:
        drawasteroid(screen, a)

def drawtrail(screen, t):
    screen.set_at((t.x, t.y), t.color)
        
def drawtrails(screen, lot):
    for t in lot:
        drawtrail(screen, t)

def render(screen, loa, trails, lot):
    drawasteroids(screen, loa)
    if trails:
        drawtrails(screen, lot)


def main():
    pygame.init()

    clock = pygame.time.Clock()
    
    t = 0
    lot = []
    loa = copy.copy(STARTCOND)

    trails = True

    pygame.display.set_caption("Newtonian Gravity Simulator")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))


    running = True
    paused = False

    while running:

        dt = clock.tick(60) /4
        t = t + dt
        

        screen.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                pos = pygame.mouse.get_pos()
                loa.append(Asteroid(pos[0], random.randint(-10,10), pos[1], random.randint(-10,10), 10, 2, (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    trails = not trails
                    lot = []
                if event.key == pygame.K_c:
                    loa = copy.deepcopy(TWOOBJECTSPINORBIT)
                    lot = []
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        if not paused:
            temp = nextasteroids(loa, lot, trails)
            loa = temp[0]
            lot = temp[1]
        render(screen, loa, trails, lot)

        pygame.display.flip()
        pygame.display.update()

main()
