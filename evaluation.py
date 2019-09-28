import numpy as np
import game
from game import main

np.random.seed(1984)

def train(model, steps, gamma):
    for asdfghjkl in range(steps):
        games = []
        lastGame=game.Game()
        scores = []
        lost=False
        after = [0,0,0]
        while not lost:
            inpScores=[0,0,0,0,0]
            for i in range(6):
                inTest = [j==i for j in range(5)]
                inpScores[i]=model.predict([[[game.getGameState(lastGame)+inTest]]])
            moves = inpScores.index(max(inpScores))
            after = game.tryUpdate(lastGame,moves)
            games += [[game.getGameState(lastGame),moves]]
            lastGame=after[0]
            if after[1] or after[2]:
                pt = after[1] - 20*after[2]
                for i in range(len(scores)):
                    scores[-1-i] += pt*gamma**i
            if after[2]:
                lost=True
        print(sum(scores)/len(scores))
        model.fit([[[[games[i][0]+games[i][1]]] for i in range(len(games))]],[[[i] for i in scores]], epochs=50)
