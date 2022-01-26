from this import d
import pygame
import copy
from pygame import gfxdraw
import random
import math

""" !!!!!!!!!!!!!!   WISHLIST   !!!!!!!!!!!!!!!!
    1) Object Trails                 DONE
    2) Add objects with mouse events DONE
    3) Slider for time               DONE
    4) Reverse time?????             SCRAPPED
    5) Collisions                    DONE
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

#Gravitational Constant
G = 1

# Size of Screen
HEIGHT = 800
WIDTH = 1000


class Particle:
    def __init__(self, x, dx, y, dy, m, r, color, charge):
        self.x = x
        self.dx = dx
        self.y = y
        self.dy = dy
        self.m = m
        self.r = r
        self.color = color
        self.charge = charge
        self.trail = []

    def colliding(self, a):
        return not bool(self.r + a.r < abs(math.hypot(abs(self.x - a.x), abs(self.y - a.y))))
    
    def nextparticle(self, oldloa, dt, trails):
        for old in oldloa:
            # Not objects on themselves(would be dividing by 0)
            hypotenuse = (math.hypot(abs(self.x - old.x), abs(self.y - old.y)))
            if (self.x == old.x and self.y == old.y):
                accel = 0
                theta = 0
            else:
                if (hypotenuse < self.r):
                    hypotenuse = self.r / 2
                accel = (G * old.m) / (hypotenuse ** 2)
                theta = math.atan2((self.x - old.x), (self.y - old.y))
                    
                ax = accel * math.sin(theta)
                ay = accel * math.cos(theta)

                self.dx = self.dx - ax * dt
                self.dy = self.dy - ay * dt
        
        # Stepping forward position with velocity 
        for b in oldloa:
            if self.colliding(b) and (not (self == b)):
                if self.m >= b.m:
                    self.dx = (self.m * self.dx + b.m * b.dx)/ (self.m+b.m)
                    self.dy = (self.m * self.dy + b.m * b.dy)/ (self.m+b.m)
                    self.m += b.m
                    self.r = round(math.sqrt(self.r**2 + b.r**2))
                    self.color = ((self.color[0]*self.m+b.color[0]*b.m)/((self.m+b.m)),
                                (self.color[1]*self.m+b.color[1]*b.m)/((self.m+b.m)),
                                (self.color[2]*self.m+b.color[2]*b.m)/((self.m+b.m)))

        # Check to add trails or not
        if trails:
            self.trail.append(ParticleTrail(int(self.x), int(self.y)))

        # Step Forward Position
        self.x = self.x + self.dx * dt
        self.y = self.y + self.dy * dt


        
        


    
    
class ParticleTrail:
    def __init__(self, x, y):
        self.x = x
        self.y = y


        
# Example Asteroids
AST0 = Particle(WIDTH / 2 - 200, 0, HEIGHT / 2, 10, 1000,
                4, WHITE, 0)
AST1 = Particle(WIDTH / 2, 0, HEIGHT / 2, 0, 10000,
                10, YELLOW, 0)
AST2 = Particle(WIDTH / 2 + 200, 0, HEIGHT / 2, -10, 1000,
                4, WHITE, 0)

# Starting Presets
CIRCULARORBIT = [Particle(WIDTH / 2 - 100, 0, HEIGHT / 2, 22, 500,
                               4, WHITE, 0),
                      Particle(WIDTH / 2, 0, HEIGHT / 2, -0.22, 50000,
                               10, YELLOW, 0)]

THREEBODYORBIT = [Particle(WIDTH / 2 - 50, 0, HEIGHT / 2, 11/1.5 , 3000,
                           2, RED, 0),
                  Particle(WIDTH / 2, 0, HEIGHT / 2, -9.3/1.5, 10000,
                           10, YELLOW, 0),
                  Particle(WIDTH / 2 + 50, 0, HEIGHT / 2, 20/1.5, 3000,
                           2, WHITE, 0)]

TWOOBJECTSPINORBIT = [Particle(WIDTH / 2 - 75, 0, HEIGHT / 2, 7, 10000,
                               5, RED, 0),
                      Particle(WIDTH / 2 + 75, 0, HEIGHT / 2, -7, 10000,
                               5, YELLOW, 0)]

COLLISION = [Particle(WIDTH / 2 + 200, -2, HEIGHT / 2, 0, 1000,
                               10, WHITE, 0),
                      Particle(WIDTH / 2 - 200, 7, HEIGHT / 2, 0, 1000,
                               10, YELLOW, 0)]

BLACKHOLE = [Particle(WIDTH / 2, 0, HEIGHT / 2, 0, 500000,
                               10, WHITE, 0)]

UNSTABLESUNPLANETMOON = [Particle(WIDTH / 2 - 300, 0, HEIGHT / 2, 13, 500,
                               4, BLUE, 0),
                      Particle(WIDTH / 2, 0, HEIGHT / 2, -0.13, 50000,
                               10, YELLOW, 0),
                      Particle(WIDTH / 2 - 315, 0, HEIGHT / 2, 18, 10**-40,
                               1, GRAY, 0)]


REALSOLARSYSTEM = [Particle(WIDTH / 2 - 300, 0, HEIGHT / 2, 2, 5.972*10**24,
                               4, BLUE, 0),
                      Particle(WIDTH / 2, 0, HEIGHT / 2, -0.13, 2*10**30,
                               10, YELLOW, 0),
                      Particle(WIDTH / 2 - 315, 0, HEIGHT / 2, 18, 7.3476*10**22,
                               1, GRAY, 0)]

TWINSUN = [Particle(WIDTH / 2 - 300, 0, HEIGHT / 2, 13, 500,
                               4, BLUE, 0),
                      Particle(WIDTH / 2 - 50, 0, HEIGHT / 2, 10 - .13/2, 25000,
                               10, YELLOW, 0),
                      Particle(WIDTH / 2 + 50, 0, HEIGHT / 2, -10 - .13/2, 25000,
                               10, GREEN, 0),
                      Particle(WIDTH / 2 - 315, 0, HEIGHT / 2, 18, 10**-40,
                               1, GRAY, 0)]

# Start Conditions
STARTCOND = TWINSUN


def dist(one, two):
    return math.hypot((one.x - two.x), (one.y - two.y))



def drawasteroid(screen, a):
    gfxdraw.circle(screen, int(a.x), int(a.y), a.r, a.color)
    gfxdraw.filled_circle(screen, int(a.x), int(a.y), a.r, a.color)


def drawasteroids(screen, loa):
    for a in loa:
        drawasteroid(screen, a)
        for t in a.trail:
            screen.set_at((t.x, t.y), a.color)

def render(screen, loa, trails):
    drawasteroids(screen, loa)



def main():
    pygame.init()

    clock = pygame.time.Clock()
    
    t = 0
    speed = (1/500)
    loa = copy.copy(STARTCOND)


    pygame.display.set_caption("Newtonian Gravity Simulator")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    running = True
    paused = False
    trails = True
    reverse = False

    while running:

        dt = clock.tick(60) * speed

        if reverse:
            dt = -abs(dt)
        t = t + dt
        

        screen.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            # Only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # Change the value to False, to exit the main loop
                running = False

            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                pos = pygame.mouse.get_pos()
                loa.append(Particle(pos[0], random.randint(-10,10), pos[1], random.randint(-10,10), 10, 2, (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), 0))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    trails = not trails
                    for a in loa:
                        a.trail = []
                if event.key == pygame.K_c:
                    loa = []
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_1:
                    loa = copy.deepcopy(TWOOBJECTSPINORBIT)
                if event.key == pygame.K_2:
                    loa = copy.deepcopy(CIRCULARORBIT)
                if event.key == pygame.K_3:
                    loa = copy.deepcopy(THREEBODYORBIT)
                if event.key == pygame.K_4:
                    loa = copy.deepcopy(COLLISION)
                if event.key == pygame.K_5:
                    loa = copy.deepcopy(BLACKHOLE)
                if event.key == pygame.K_6:
                    loa = copy.deepcopy(UNSTABLESUNPLANETMOON)
                if event.key == pygame.K_EQUALS:
                    speed = speed * 1.1
                if event.key == pygame.K_MINUS:
                    speed = speed * (1/1.1)
        if not paused:   
            for a in loa:
                # Remove elements far away from screen
                if abs(a.x - (WIDTH / 2)) > 2 * WIDTH or abs(a.y - (HEIGHT / 2)) > 2 * HEIGHT:
                    loa.remove(a)
                for b in loa.copy():
                    if a.colliding(b) and a.m > b.m:
                        loa.remove(b)
                a.nextparticle(loa, dt, trails)

        render(screen, loa, trails)

        pygame.display.flip()
        pygame.display.update()

if __name__ == "__main__":
    main()
