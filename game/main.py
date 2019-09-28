import sys, pygame, os
import numpy as np

class TileMap:
        def __init__(self, width, height, images, tileSize):
                self.width = width
                self.height = height

                self.images = images
                self.tileSize = tileSize

                self.data = [[0 for x in range(self.width)] for y in range(self.height)]

        def draw(self, surface, ox, oy):
                for y in range(self.height):
                        for x in range(self.width):
                                if self.data[y][x] > 0:
                                        surface.blit(self.images[self.data[y][x] - 1], (ox + (x * self.tileSize), oy + (y * self.tileSize)))


class Board:
        def __init__(self):
                print(os.getcwd())
                self.tileMap = TileMap(10, 20, [pygame.image.load(os.path.dirname(os.path.abspath(f"resources/{x}.png"))+f"\\{x}.png") for x in range(1, 8)], 24)
        def tileOnBoard(self, x, y):
                return x >= 0 and y >= 0 and x < self.tileMap.width and y < self.tileMap.height

        def boardCoordsToTileCoords(self, x, y):
                return [x, self.tileMap.height - y - 1]

        def getTileAt(self, x, y):
                if not self.tileOnBoard(x, y):
                        return 1
                x, y = self.boardCoordsToTileCoords(x, y)
                return self.tileMap.data[y][x]

        def setTileAt(self, x, y, tile):
                if not self.tileOnBoard(x, y):
                        return
                x, y = self.boardCoordsToTileCoords(x, y)
                self.tileMap.data[y][x] = tile

        def draw(self, surface):
                self.tileMap.draw(surface, 0, 0)

        def getBoringBoard(self):
                return [[(self.tileMap.data[y][x] > 0) for x in range(self.width)] for y in range(self.height)]

class PieceData:
        TetrominoTable = [
                [ (-1, 0), ( 0, 0), ( 1, 0), ( 2, 0) ], # I
                [ (-1, 1), (-1, 0), ( 0, 0), ( 1, 0) ], # J
                [ ( 1, 1), (-1, 0), ( 0, 0), ( 1, 0) ], # L
                [ ( 0, 1), ( 1, 1), ( 0, 0), ( 1, 0) ], # O
                [ ( 0, 1), ( 1, 1), (-1, 0), ( 0, 0) ], # S
                [ ( 0, 1), (-1, 0), ( 0, 0), ( 1, 0) ], # T
                [ (-1, 1), ( 0, 1), ( 0, 0), ( 1, 0) ], # Z
                ]
        RotationTable = []

        def rotatePoint(p, r):
                if r == 0:
                        return p
                elif r == 1:
                        return (p[1], -p[0])
                elif r == 2:
                        return (-p[0], -p[1])
                elif r == 3:
                        return (-p[1], p[0])

        def getPiece(tetromino, rotation):
                s=0#TODO: this function will return the piece as an array of tuples representing points.

class Piece:
        x = 0
        y = 0

        tetromino = 0
        rotation = 0

        #TODO: the constructor for this

# Start pygame.
pygame.init()

# Initialize some cool values.
width, height = 24*10, 24*20
size = (width, height)

# Get the screen surface, which is a thing we can use to draw stuff.
screen = pygame.display.set_mode(size)

# NOTE: This is using screen coordinates. +Y is down internally, but my wrapper functions for the board will automatically convert the coordinates into board coordinates.
board = Board()

while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        sys.exit()

        screen.fill((0, 0, 0))
        board.draw(screen)
        pygame.display.flip()
