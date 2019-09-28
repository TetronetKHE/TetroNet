import numpy as np

class gameState:
    def __init__(self, staticMatrix, pieceID, rotation, position):
        self.static = staticMatrix  #10x20 matrix
        self.piece = pieceID        #0-6
        self.rotation = rotation    #r 0-3
        self.pos = position         #[x,y] x 0-9 y 0-19
    def __mul__(self, inpt):
        self #change necessary things
        return [rows, lose] #rows is number of rows dele

np.random.seed(1984)

def getStart():
    true=False #make a random start

games = []
scores = []

