import numpy as np

def copyMat(a):
    n=[[j for j in i] for i in a]
    return n

class gameState:
    def __init__(self, staticMatrix, pieceID, rotation, position, queued):
        self.static = staticMatrix  #10x20 matrix
        self.piece = pieceID        #0-6
        self.rotation = rotation    #r 0-3
        self.pos = position         #[x,y] x 0-9 y 0-19
        self.nexts = queued         #[ID, ID, ID]
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
        a+=self.nexts
        return a

np.random.seed(1984)

def getStart():
    true=False #make a random start

def train(model, steps, gamma):
    for asdfghjkl in range(steps):
        games = [[getStart(),[0,0,0,0,0]]
        scores = [0]
        lost=False
        after = [0,0,0]
        while not lost:
            lstGame=games[-1][0]
            inpScores=[0,0,0,0,0]
            for i in range(6):
                inTest = [j==i for j in range(5)]
                inpScores[i]=model.predict([[[lstGame.toList()+inTest]]])
            moves = inpScores.index(max(inpScores))
            after = lstGame*moves
            games += [[after[0],moves]]
            if after[1] or after[2]:
                pt = after[1] - 20*after[2]
                for i in range(len(scores)):
                    scores[-1-i] += pt*gamma**i
            if after[2]:
                lost=True
        model.fit([[[[games[i][0].toList()+games[i][1]]] for i in range(len(games))]],[[[i] for i in scores]], epochs=50)
