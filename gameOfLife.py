import sys
import random

import pygame

from colours import dark_blue, green, black
from patterns import glider, rPentomino, dieHard


def drawGrid():
    for x in range(0, width, cellSize):
        pygame.draw.line(screen, dark_blue, (x, 0), (x, height))
    for y in range(0, height, cellSize):
        pygame.draw.line(screen, dark_blue, (0, y), (width, y))


def getCells(density=0.2):
    return {(c, r): random.random() < density for c in range(columns) for r in range(rows)}


def getPatternCells(pattern):
    # Set all to False
    cells = {(c, r): False for c in range(columns) for r in range(rows)}

    # print glider
    # print glider[0]

    # Loop through the pattern string
    for idx, g in enumerate(pattern):

        # print "Index : %s" % idx
        # print "Number : %s" % g
        #Then loop through 5 x 5 mini-grid
        # for col in range(5):
        if g == "1":
            cells[(idx % 5, idx // 5)] = True

    # for x in range(5):
    #    for y in range(5):
    #        print("(" + str(y) + ", " + str(x) + ") :  "),
    #        print cells[(y, x)]

    return cells


def drawCells():
    for(x, y) in cells:
        colour = green if cells[x, y] else black
        rectangle = (x * cellSize, y * cellSize, cellSize, cellSize)
        pygame.draw.rect(screen, colour, rectangle)


def getNeighbours((x, y)):
    positions = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                    (x - 1, y), (x + 1, y),
                 (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
                 ]

    return [cells[r, c] for (r, c) in positions if 0 <= r < rows and 0 <= c < columns]

def evolve():
    global cells

    newCells = cells.copy()

    for position, alive in cells.items():
        liveNeighbours = sum(getNeighbours(position))
        if alive:
            if liveNeighbours not in [2, 3]:
                newCells[position] = False
        elif liveNeighbours == 3:
                newCells[position] = True

    cells = newCells


pygame.init()
columns, rows = 50, 50
cellSize = 10
size = width, height = columns * cellSize, rows * cellSize
screen = pygame.display.set_mode(size)

# cells = getCells()
# cells = getPatternCells(glider)
# cells = getPatternCells(rPentomino)
cells = getPatternCells(dieHard)

clock = pygame.time.Clock()

speed = 2
rate = 0.5

while True:
    # Check which keys are pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        # Increasing the clock tick speed moves the game faster
        speed += rate
    elif keys[pygame.K_DOWN]:
        # Reducing the clock tick speed moves the game slower
        speed -= rate

    print "Clock Speed :  %s" % speed
    clock.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    drawCells()
    # pygame.time.wait(5000)
    evolve()
    drawGrid()
    # pygame.time.wait(5000)

    pygame.display.update()