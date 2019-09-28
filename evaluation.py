import numpy as np
import game

np.random.seed(1984)

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
