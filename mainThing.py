import pygame
import math


# Color Constants
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BLUE = (0,   0,   255)
GREEN = (0,   255, 0)
RED = (255, 0,   0)
YELLOW = (0,   255, 255)

# Speed and Gravitational Constant
DT = .1
G = 30

# Size of
HEIGHT = 600
WIDTH = 1000


class Asteroid:
    def __init__(self, x, dx, y, dy, m, r, color) -> None:
        self.x = x
        self.dx = dx
        self.y = y
        self.dy = dy
        self.m = m
        self.r = r
        self.color = color


AST0 = Asteroid(WIDTH / 2 - 200, 0, HEIGHT / 2, 10, 10,
                4, WHITE)
AST1 = Asteroid(WIDTH / 2, 0, HEIGHT / 2, 0, 1000,
                10, YELLOW)
AST2 = Asteroid(WIDTH / 2 + 200, 0, HEIGHT / 2, -10, 10,
                4, WHITE)

STABLETWOBODYORBIT = [Asteroid(WIDTH / 2 - 200, 0, HEIGHT / 2, 10, 10,
                               4, WHITE),
                      Asteroid(WIDTH / 2, 0, HEIGHT / 2, -0.1, 1000,
                               10, YELLOW)]

THREEBODYORBIT = [Asteroid(WIDTH / 2 - 200, 0, HEIGHT / 2, 10, 10,
                           4, WHITE),
                  Asteroid(WIDTH / 2, 0, HEIGHT / 2, 0, 1000,
                           10, YELLOW),
                  Asteroid(WIDTH / 2 + 200, 0, HEIGHT / 2, -10, 10,
                           4, WHITE)]

loa = STABLETWOBODYORBIT


def nextasteroid(a):
    a.x = a.x + DT * a.dx
    a.y = a.y + DT * a.dy
    return a


def dist(one, two):
    return math.hypot((one.x - two.x), (one.y - two.y))


def nextasteroids(loa):
    oldloa = loa
    listout = []
    for a in loa:
        for old in oldloa:
            if (a.x == old.x and a.y == old.y):
                accel = 0
                theta = 0
            else:
                accel = (G * old.m) / \
                    ((math.hypot(abs(a.x - old.x), abs(a.y - old.y))) ** 2)
                theta = math.atan2((a.x - old.x), (a.y - old.y))

            ax = accel * math.sin(theta)
            ay = accel * math.cos(theta)

            a.dx = a.dx - ax * DT
            a.dy = a.dy - ay * DT

        listout.append(a)

    for a in listout:
        a = nextasteroid(a)
    return listout


def main():
    pygame.init()

    t = 0

    pygame.display.set_caption("Newtonian Gravity Simulator")

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def drawasteroid(a):
        pygame.draw.circle(screen, a.color, (a.x, a.y), a.r)

    def drawasteroids(loa):
        for a in loa:
            drawasteroid(a)

    running = True

    while running:

        t = t + DT

        screen.fill(BLACK)

        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        drawasteroids(loa)
        nextasteroids(loa)

        pygame.display.flip()


main()
