import numpy as np

def copyMat(a):
    n=[[j for j in i] for i in a]
    return n

class gameState:
    def __init__(self, staticMatrix, pieceID, rotation, position):
        self.static = staticMatrix  #10x20 matrix
        self.piece = pieceID        #0-6
        self.rotation = rotation    #r 0-3
        self.pos = position         #[x,y] x 0-9 y 0-19
    def __mul__(self, inpt):
        mat = copyMat(self.static)
        new = gameState(mat,self.piece,self.rotation,[self.pos[0],self.pos[1]])
        new #change necessary things
        return [new,rows, lose] #rows is number of rows deleted, lose is 1 if you lost
    def toList(self):
        a=[]
        for i in self.static:
            a+=i
        a+=[self.piece]
        a+=[self.rotation]
        a+=self.pos
        return a

np.random.seed(1984)

def getStart():
    true=False #make a random start

def train(model, steps, gamma):
    for i in range(steps):
        games = [getStart()]
        scores = [0]
        lost=False
        after = [0,0]
        while not lost:
            after = games[-1]*
