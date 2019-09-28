import sys, pygame, os
import numpy as np
import random
import copy

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
Tiles = [pygame.image.load(os.path.dirname(os.path.abspath("resources/1.png"))+f"\\{x}.png") for x in range(1, 8)]

class TileMap:
        def __init__(self, width, height, tileSize):
                self.width = width
                self.height = height
                
                self.tileSize = tileSize
                
                self.data = [[0 for x in range(self.width)] for y in range(self.height)]

        def draw(self, surface, ox, oy):
                for y in range(self.height):
                        for x in range(self.width):
                                self.drawTile(surface, ox, oy, x, y, self.data[self.height - y - 1][x])
        
        def drawTile(self, surface, ox, oy, tx, ty, tile):
                if tile > 0: surface.blit(Tiles[tile - 1], (ox + (tx * self.tileSize), oy + (ty * self.tileSize)))

class Board:
        def __init__(self):
                self.tileMap = TileMap(10, 20, 24)
        
        def update(self):
                r = 0
                for y in range(self.tileMap.height - 1, -1, -1):
                        if self.lineFull(y):
                                self.clearLine(y)
                                r += 1
                return r
        
        def lineFull(self, y):
                for x in range(self.tileMap.width):
                        if not self.tileMap.data[y][x]: return False
                return True
        
        def lineEmpty(self, y):
                for x in range(self.tileMap.width):
                        if self.tileMap.data[y][x]: return False
                return True
        
        def clearLine(self, y):
                for line in range(y, self.tileMap.height - 1):
                        self.tileMap.data[line] = self.tileMap.data[line + 1]
                self.tileMap.data[self.tileMap.height - 1] = [0 for x in range(self.tileMap.width)]
        
        def tileOnBoard(self, x, y):
                return x >= 0 and y >= 0 and x < self.tileMap.width and y < self.tileMap.height
        
        def getTileAt(self, x, y):
                if not self.tileOnBoard(x, y): return 1
                return self.tileMap.data[y][x]

        def setTileAt(self, x, y, tile):
                if not self.tileOnBoard(x, y): return
                self.tileMap.data[y][x] = tile

        def draw(self, surface):
                self.tileMap.draw(surface, 0, 0)

        def getBoringBoard(self):
                return [self.tileMap.data[y][x] > 0 for x in range(self.tileMap.width) for y in range(self.tileMap.height)]

class PieceData:
        TetrominoTable = [
                [ [-1, 0], [ 0, 0], [ 1, 0], [ 2, 0] ], # I
                [ [-1, 1], [-1, 0], [ 0, 0], [ 1, 0] ], # J
                [ [ 1, 1], [-1, 0], [ 0, 0], [ 1, 0] ], # L
                [ [ 0, 1], [ 1, 1], [ 0, 0], [ 1, 0] ], # O
                [ [ 0, 1], [ 1, 1], [-1, 0], [ 0, 0] ], # S
                [ [ 0, 1], [-1, 0], [ 0, 0], [ 1, 0] ], # T
                [ [-1, 1], [ 0, 1], [ 0, 0], [ 1, 0] ], # Z
        ]
        RotationTable = {
                "I": [
                        [ [ 0, 0], [-1, 0], [ 2, 0], [-1, 0], [ 2, 0] ],
                        [ [-1, 0], [ 0, 0], [ 0, 0], [ 0, 1], [ 0,-2] ],
                        [ [-1, 1], [ 1, 1], [-2, 1], [ 1, 0], [-2, 0] ],
                        [ [ 0, 1], [ 0, 1], [ 0, 1], [ 0,-1], [ 0, 2] ]
                ],
                "O": [
                        [ [ 0, 0] ],
                        [ [ 0,-1] ],
                        [ [-1,-1] ],
                        [ [-1, 0] ]
                ],
                "Other": [
                        [ [ 0, 0], [ 0, 0], [ 0, 0], [ 0, 0], [ 0, 0] ],
                        [ [ 0, 0], [ 1, 0], [ 1,-1], [ 0, 2], [ 1, 2] ],
                        [ [ 0, 0], [ 0, 0], [ 0, 0], [ 0, 0], [ 0, 0] ],
                        [ [ 0, 0], [-1, 0], [-1,-1], [ 0, 2], [-1, 2] ]
                ]
        }
        
        def rotatePoint(p, r):
                if r == 0:
                        return p
                elif r == 1:
                        return [p[1], -p[0]]
                elif r == 2:
                        return [-p[0], -p[1]]
                elif r == 3:
                        return [-p[1], p[0]]

        def getPiecePoints(tetromino, rotation):
                result = PieceData.TetrominoTable[tetromino].copy()
                
                for i in range(len(result)):
                        result[i] = PieceData.rotatePoint(result[i], rotation)
                
                return result
        
        def getOffsetTableLength(tetromino, rotation):
                if tetromino == Tetrominos["I"]:
                        return len(PieceData.RotationTable["I"][rotation])
                elif tetromino == Tetrominos["O"]:
                        return len(PieceData.RotationTable["O"][rotation])
                else:
                        return len(PieceData.RotationTable["Other"][rotation])
        
        def getOffsetPoint(tetromino, rotation, check):
                if tetromino == Tetrominos["I"]:
                        result = PieceData.RotationTable["I"][rotation][check].copy()
                elif tetromino == Tetrominos["O"]:
                        result = PieceData.RotationTable["O"][rotation][check].copy()
                else:
                        result = PieceData.RotationTable["Other"][rotation][check].copy()
                
                return result
        
        def getOffset(tetromino, prevRot, rotation, check):
                prevOffset = PieceData.getOffsetPoint(tetromino, prevRot, check)
                nextOffset = PieceData.getOffsetPoint(tetromino, rotation, check)
                
                return (prevOffset[0] - nextOffset[0], prevOffset[1] - nextOffset[1])

class Piece:
        MaxLockDelay = 4
        MaxMoveReset = 8
        MaxSpins = 16
        
        def __init__(self, board, tetromino):
                self.x = 4
                self.y = 18
                
                self.board = board
                
                self.tetromino = tetromino
                self.rotation = 0
                
                self.lockDelay = Piece.MaxLockDelay
                
                self.points = PieceData.getPiecePoints(self.tetromino, self.rotation)
                
                self.moveResets = Piece.MaxMoveReset
                self.spinsLeft = Piece.MaxSpins
                
                self.down = False
        
        def update(self, inputs):
                if inputs[0]: self.tryMove(-1, 0)
                if inputs[1]: self.tryMove(1, 0)
                
                if (not self.moveResets) and (not self.lockDelay) and (not self.fit(0, -1)):
                        self.placeDown()
                
                if inputs[2] and self.spinsLeft:
                        self.tryRotation(False)
                        self.spinsLeft -= 1
                if inputs[3] and self.spinsLeft:
                        self.tryRotation(True)
                        self.spinsLeft -= 1
                
                if inputs[4]:
                        self.y = self.getYDropCoord()
                        self.placeDown()
                elif self.tryMove(0, -1):
                        if self.moveResets:
                                self.lockDelay = Piece.MaxLockDelay
                                self.moveResets -= 1
                else:
                        if self.lockDelay:
                                self.lockDelay -= 1
                        else:
                                self.placeDown()
        
        def draw(self, surface):
                for i in range(len(self.points)):
                        self.board.tileMap.drawTile(surface, 0, 0, self.x + self.points[i][0], self.board.tileMap.height - self.y - self.points[i][1] - 1, self.tetromino + 1)
        
        def fitAbsolute(self, x, y): # Check if piece fits at that exact position.
                for i in range(len(self.points)):
                        if self.board.getTileAt(x + self.points[i][0], y + self.points[i][1]): return False
                return True
        
        def fit(self, x, y): # Check if piece fits at that position relative to the piece.
                return self.fitAbsolute(self.x + x, self.y + y)
        
        def tryMove(self, x, y):
                if self.fit(x, y):
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
        
        def placeDown(self):
                for i in range(len(self.points)):
                        self.board.setTileAt(self.x + self.points[i][0], self.y + self.points[i][1], self.tetromino + 1)
                self.down = True
        
        def getYDropCoord(self):
                tmpY = self.y
                
                while True:
                        if self.fitAbsolute(self.x, tmpY - 1):
                                tmpY -= 1
                        else:
                                return tmpY
        
        def getBoringPiece(self):
                return [self.tetromino, self.rotation, self.x, self.y]
        
        def getBoringPiece2(self):
                p = [self.x, self.y]
                return [p[d]+self.points[pt][d] for d in range(2) for pt in range(len(self.points))]

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
        
        def __init__(self):
                self.bag = Bag()
                self.getNewQueue()
        
        def getNewQueue(self):
                self.queue = [self.bag.getPiece() for i in range(NextQueue.MaxNext)]
        
        def getPiece(self):
                self.queue.append(self.bag.getPiece())
                return self.queue.pop(0)
        
        def getBoringNext(self):
                return self.queue.copy()
        
        def getBoringNext2(self):
                tmpPts = getPiecePoints(self.queue[0], 0)
                return [tmpPts[pt][d] for d in range(2) for pt in range(len(tmpPts))]

class Game:
        def __init__(self):
                self.board = Board()
                self.nextQueue = NextQueue()
                self.piece = Piece(self.board, self.nextQueue.getPiece())
                
                self.gameOver = False
        
        def update(self, inputs):
                if self.gameOver: return
                
                self.piece.update(inputs)
                if self.piece.down: self.piece = Piece(self.board, self.nextQueue.getPiece())
                if not self.piece.fit(0, 0): self.gameOver = True
                self.linesCleared = self.board.update()
        
        def draw(self, surface):
                self.board.draw(surface)
                self.piece.draw(surface)

def getGameState(game):
        result = []
        result += game.board.getBoringBoard()
        result += game.piece.getBoringPiece2()
        result += game.nextQueue.getBoringNext2()
        return result

def tryUpdate(game, inputs):
        tmpGame = copy.deepcopy(game)
        tmpGame.update(inputs)
        return tmpGame, tmpGame.linesCleared, tmpGame.gameOver

def drawGame(game):
        screen.fill((0, 100, 0))
        game.draw(screen)
        pygame.display.flip()

human_mode = False

# Start pygame.
pygame.init()

# Initialize some cool values.
width, height = 24*10, 24*20
size = (width, height)

# Get the screen surface, which is a thing we can use to draw stuff.
screen = pygame.display.set_mode(size)

frame = 0

if human_mode:
        game = Game()
        inputs = [0, 0, 0, 0, 0]
        
        while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                sys.exit()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_LEFT: inputs[0] = True
                                if event.key == pygame.K_RIGHT: inputs[1] = True
                                if event.key == pygame.K_z: inputs[2] = True
                                if event.key == pygame.K_x: inputs[3] = True
                                if event.key == pygame.K_UP: inputs[4] = True
                        if event.type == pygame.KEYUP:
                                if event.key == pygame.K_LEFT: inputs[0] = False
                                if event.key == pygame.K_RIGHT: inputs[1] = False
                                if event.key == pygame.K_z: inputs[2] = False
                                if event.key == pygame.K_x: inputs[3] = False
                                if event.key == pygame.K_UP: inputs[4] = False
                
                if frame % 60 == 0: game.update(inputs)
                # if frame % 60*8 == 0: print(game.board.getBoringBoard())
                
                drawGame(game)
                frame += 1
