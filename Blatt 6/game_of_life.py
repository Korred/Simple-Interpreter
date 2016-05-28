
# Aufgabe 3 - Pygame

import pygame
import sys

def lifestep(cells):
    "perform one life step for the current generation"
    nextGen = set([])
    # alive
    for c in cells:
        tempNeighbors = getNeighbors(c)
        neighbors = cells.intersection(tempNeighbors)
        if (len(neighbors) in set([2,3])):
            # stay alive
            nextGen.add(c)
    if (cells != set([])):
        tempX = [t[0] for t in cells]
        tempY = [t[1] for t in cells]
        minX,maxX = getMinMax(tempX)
        minY,maxY = getMinMax(tempY)
        for dx in range(minX-1,maxX+2):     # expand for border cells
            for dy in range(minY-1,maxY+2):
                # reborn
                if (len(cells.intersection(getNeighbors((dx,dy)))) == 3):
                    nextGen.add((dx,dy))
    return nextGen

def getNeighbors(cell):
    x = cell[0]
    y = cell[1]
    neighbors = set([])
    for dx in set([-1,0,1]):
        for dy in set([-1,0,1]):
            if not ((dx,dy) == (0,0)):
                neighbors.add((x+dx,y+dy))
    return neighbors

def getMinMax(list):
    return min(list),max(list)

def lifestring(cells):
    "return the current generation as a string representing the board"
    if (cells == set([])):
        return ""
    else:
        tempX = [t[0] for t in cells]
        tempY = [t[1] for t in cells]
        minX,maxX = getMinMax(tempX)
        minY,maxY = getMinMax(tempY)
        board = ""
        for dy in range(minY,maxY+1):
            for dx in range(minX,maxX+1):
                if ((dx,dy) in cells):
                    board += "X"
                else:
                    board += " "
            if ((maxY > 0) & (dy != maxY)):
                board += "\n"        
        return board

def from_lifestring(lifestring):
    "return a set of cells for a given life string"
    x,y = 0,0
    cells = set([])
    for c in lifestring:
        if (c == "X"):
            cells.add((x,y))
        x += 1
        if (c == "\n"):
            y += 1
            x = 0
    return cells

def main(cells):
    "graphical viewer for Game of Life"
    screen, bg, clock = initScreen()
    while True:
        clock.tick(60)
        cells = lifestep(cells)
        for pos in cells:
            pygame.draw.circle(bg,(255,255,40),(pos[0]+200,pos[1]+200),1,1)
        screen.blit(bg,(0,0))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return

def initScreen():
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption("Game of Life")
    bg = pygame.Surface((500,500))
    clock = pygame.time.Clock()
    return screen, bg, clock

input = sys.argv

with open(input[1], 'r') as myfile:
    lifestring=myfile.read()
cells = from_lifestring(lifestring)
main(cells)