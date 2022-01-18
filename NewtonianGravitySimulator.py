from operator import truediv
import pygame
import random
#import pygame_widgets
#import StackoverflowSlider

#from pygame_widgets.slider import Slider
#from pygame_widgets.textbox import TextBox
import math



""" !!!!!!!!!!!!!!   WISHLIST   !!!!!!!!!!!!!!!!
1) Object Trails
2) Add objects with mouse events
3) Slider for time
4) reverse time?????

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
DT = 0.1
G = 40

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

THREEBODYORBIT = [Asteroid(WIDTH / 2 - 200, 0, HEIGHT / 2, 11 , 300,
                           6, RED),
                  Asteroid(WIDTH / 2, 0, HEIGHT / 2, 0, 3000,
                           10, YELLOW),
                  Asteroid(WIDTH / 2 + 200, 0, HEIGHT / 2, 20, 10,
                           4, WHITE)]

TWOOBJECTSPINORBIT = [Asteroid(WIDTH / 2 - 75, 0, HEIGHT / 2, 2, 100,
                               10, BLUE),
                      Asteroid(WIDTH / 2 + 75, 0, HEIGHT / 2, -2, 100,
                               10, YELLOW)]

COLLISION = [Asteroid(WIDTH / 2 + 200, -2, HEIGHT / 2, 0, 100,
                               10, WHITE),
                      Asteroid(WIDTH / 2 - 200, 7, HEIGHT / 2, 0, 10,
                               10, YELLOW)]

STARTCOND = TWOOBJECTSPINORBIT


def nextasteroid(a):
    a.x = a.x + DT * a.dx
    a.y = a.y + DT * a.dy
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

            a.dx = a.dx - ax * DT
            a.dy = a.dy - ay * DT
            
        #ke= ke + (1/2) * a.m * (a.dx**2+a.dy**2) 
        

        listout.append(a)
    
    #print(ke)
    #print(pe)
    #print(ke + pe)
    #print("---------------------")

    
    #Stepping forward position with velocity 
    for a in listout:
        a = nextasteroid(a)
        if trails:
            lot.append(AsteroidTrail(int(a.x), int(a.y), a.color))
    return (listout, lot)


def drawasteroid(screen, a):
    pygame.draw.circle(screen, a.color, (a.x, a.y), a.r)


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
    loa = STARTCOND

    trails = True

    pygame.display.set_caption("Newtonian Gravity Simulator")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))


    running = True

    while running:

        DT = clock.tick(60)
        t = t + DT
        

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
                loa.append(Asteroid(pos[0], 0, pos[1], 0, 10, 4, (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    trails = not trails
                    lot = []
                if event.key == pygame.K_c:
                    lot = []
        
            
        render(screen, loa, trails, lot)
        temp = nextasteroids(loa, lot, trails)
        loa = temp[0]
        lot = temp[1]

        pygame.display.flip()
        pygame.display.update()

main()
