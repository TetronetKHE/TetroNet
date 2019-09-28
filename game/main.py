import sys, pygame, os
import numpy as np
import random
import copy

import tilemap, board, piecedata

Tetrominos = {
        "I" : 0,
        "J" : 1,
        "L" : 2,
        "O" : 3,
        "S" : 4,
        "T" : 5,
        "Z" : 6,
        "Length": 7
}

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
                                self.drawTile(surface, ox, oy, x, y, self.data[y][x])
        
        def drawTile(self, surface, ox, oy, tx, ty, tile):
                if tile > 0: surface.blit(self.images[tile - 1], (ox + (tx * self.tileSize), oy + (ty * self.tileSize)))


class Board:
        def __init__(self):
                self.tileMap = TileMap(10, 20, [pygame.image.load(f"resources\\{x}.png") for x in range(1, 8)], 24)
        
        def tileOnBoard(self, x, y):
                return x >= 0 and y >= 0 and x < self.tileMap.width and y < self.tileMap.height

        def boardCoordsToTileCoords(self, x, y):
                return [x, self.tileMap.height - y - 1]

        def getTileAt(self, x, y):
                if not self.tileOnBoard(x, y): return 1
                x, y = self.boardCoordsToTileCoords(x, y)
                return self.tileMap.data[y][x]

        def setTileAt(self, x, y, tile):
                if not self.tileOnBoard(x, y): return
                x, y = self.boardCoordsToTileCoords(x, y)
                self.tileMap.data[y][x] = tile

        def draw(self, surface):
                self.tileMap.draw(surface, 0, 0)

        def getBoringBoard(self):
                return [((self.tileMap.data[y][x] > 0) for x in range(self.width)) for y in range(self.height)]

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
        RotationTable = {
                "I": [
                        [ ( 0, 0), (-1, 0), ( 2, 0), (-1, 0), ( 2, 0) ],
                        [ (-1, 0), ( 0, 0), ( 0, 0), ( 0, 1), ( 0,-2) ],
                        [ (-1, 1), ( 1, 1), (-2, 1), ( 1, 0), (-2, 0) ],
                        [ ( 0, 1), ( 0, 1), ( 0, 1), ( 0,-1), ( 0, 2) ]
                ],
                "O": [
                        [ ( 0, 0) ],
                        [ ( 0,-1) ],
                        [ (-1,-1) ],
                        [ (-1, 0) ]
                ],
                "Other": [
                        [ ( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0) ],
                        [ ( 0, 0), ( 1, 0), ( 1,-1), ( 0, 2), ( 1, 2) ],
                        [ ( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0) ],
                        [ ( 0, 0), (-1, 0), (-1,-1), ( 0, 2), (-1, 2) ]
                ]
        }
        
        def rotatePoint(p, r):
                if r == 0:
                        return p
                elif r == 1:
                        return (p[1], -p[0])
                elif r == 2:
                        return (-p[0], -p[1])
                elif r == 3:
                        return (-p[1], p[0])

        def getPiecePoints(tetromino, rotation):
                result = PieceData.TetrominoTable[tetromino].copy()
                
                for i in range(len(result)):
                        result[i] = PieceData.rotatePoint(result[i], rotation)
                
                return result
        
        def getOffsetTableLength(tetromino, rotation):
                if tetromino == Tetrominos["I"]:
                        return len(PieceData.RotationTable["I"])
                elif tetromino == Tetrominos["O"]:
                        return len(PieceData.RotationTable["O"])
                else:
                        return len(PieceData.RotationTable["Other"])
        
        def getOffsetPoint(tetromino, rotation, check):
                if tetromino == Tetrominos["I"]:
                        result = PieceData.RotationTable["I"][check].copy()
                elif tetromino == Tetrominos["O"]:
                        result = PieceData.RotationTable["O"][check].copy()
                else:
                        result = PieceData.RotationTable["Other"][check].copy()
                
                return result
        
        def getOffset(tetromino, prevRot, rotation, check):
                prevOffset = PieceData.getOffsetPoint(tetromino, rotation, check)
                nextOffset = PieceData.getOffsetPoint(tetromino, rotation, check)
                
                return (prevOffset[0] - nextOffset[0], prevOffset[1] - nextOffset[1])

class Piece:
        MaxLockDelay = 4
        
        def __init__(self, board, tetromino):
                self.x = 4
                self.y = 20
                
                self.board = board
                
                self.tetromino = tetromino
                self.rotation = 0
                
                self.lockDelay = Piece.MaxLockDelay
                
                self.points = PieceData.getPiecePoints(self.tetromino, self.rotation)
        
        def update(self, inputs):
                if inputs[0]: self.tryMove(-1, 0)
                if inputs[1]: self.tryMove(1, 0)
                
                if inputs[2]: self.tryRotation(False)
                if inputs[3]: self.tryRotation(True)
                
                if inputs[4]:
                        self.y = self.getYDropCoord()
                elif tryMove(0, -1):
                        self.lockDelay = Piece.MaxLockDelay
                else:
                        if self.lockDelay:
                                self.lockDelay -= 1
                        else:
                                self.placeDown()
        
        def draw(self, surface):
                for i in range(len(points)):
                        self.board.drawTile(surface, 0, 0, self.x + self.points[i][0], self.x + self.points[i][1], self.tetromino)
        
        def fitAbsolute(self, x, y): # Check if piece fits at that exact position.
                for i in range(len(points)):
                        if not self.board.getTileAt(x, y): return False
                return True
        
        def fit(self, x, y): # Check if piece fits at that position relative to the piece.
                return self.fitAbsolute(self.x + x, self.y + y)
        
        def tryMove(self, x, y):
                if fit(self, x, y):
                        self.x += x
                        self.y += y
                        return True
                return False
                
        def tryRotation(self, clockwise):
                prevRot = self.rotation
                if clockwise:
                        self.rotation = (self.rotation + 1) % 4
                else:
                        self.rotation = (self.rotation + 3) % 4
                self.points = PieceData.getPiecePoints(self.tetromino, self.rotation)
                
                for i in range(PieceData.getOffsetTableLength(self.tetromino, self.rotation)):
                        offset = PieceData.getOffset(self.tetromino, prevRot, self.rotation, i)
                        
                        if self.fit(offset[0], offset[1]):
                                self.x += offset[0]
                                self.y += offset[1]
                                return True
                        
                self.rotation = prevRot
                self.points = PieceData.getPiecePoints(self.tetromino, self.rotation)
                
                return False
        
        def getYDropCoord(self):
                tmpY = self.y
                
                while True:
                        if self.fitAbsolute(self.x, tmpY - 1):
                                tmpY -= 1
                        else:
                                return tmpY
        
        def getBoringPiece(self):
                return [self.tetromino, self.rotation, self.x, self.y]

class Bag:
        def __init__(self):
                self.getNewBag()
        
        def getNewBag(self):
                self.bag = [i for i in range(Tetrominos["Length"])]
                random.shuffle(self.bag)
        
        def getPiece(self):
                if not len(self.bag): self.getNewBag()
                return self.bag.pop(0)

class NextQueue:
        MaxNext = 3
        
        def __init__(self, bag):
                self.bag = bag
                self.getNewQueue()
        
        def getNewQueue(self):
                self.queue = [self.bag.getPiece() for i in range(NextQueue.MaxNext)]
        
        def getPiece(self):
                if not len(self.queue): self.getNewQueue()
                return self.queue.pop(0)
        
        def getBoringNext(self):
                return self.queue.copy()

class Game:
        def __init__(self):
                self.board = Board()
                self.bag = Bag()
                self.nextQueue = NextQueue(self.bag)
                self.piece = Piece(self.board, self.nextQueue.getPiece())
        
        def update(self, inputs):
                self.piece.update()
                if self.piece.down: self.piece = Piece(board, nextQueue.getPiece())
        
        def tryUpdate(self, inputs):
                tmpBoard = Board()
                tmpBoard.tileMap.data = [row.copy() for row in self.board.tileMap.data]
                tmpBag = Bag()
                tmpBag.bag = self.bag.bag.copy()
                tmpNextQueue = NextQueue(tmpBag)
                #TODO
                

# Start pygame.
pygame.init()

# Initialize some cool values.
width, height = 24*10, 24*20
size = (width, height)

# Get the screen surface, which is a thing we can use to draw stuff.
screen = pygame.display.set_mode(size)

# NOTE: This is using screen coordinates.  Y is down internally, but my wrapper functions for the board will automatically convert the coordinates into board coordinates.
def getANewGame():
        board = Board()
        bag = Bag()
        nextQueue = NextQueue(bag)
        piece = Piece(board, nextQueue.getPiece())
        
        return board, bag, nextQueue, piece

def getGameState(game):
        result = []
        result += board.getBoringBoard()
        result += piece.getBoringPiece()
        result += nextQueue.getBoringNext()
        return result

def tryUpdate():
        
        

board, bag, nextQueue, piece = getANewGame()

while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        sys.exit()
        
        
        screen.fill((0, 0, 0))
        board.draw(screen)
        piece.draw(screen)
        pygame.display.flip()
