import numpy as np
import game

np.random.seed(1984)

def train(model, steps, gamma):
    for asdfghjkl in range(steps):
        print("step " + str(asdfghjkl))
        games = []
        lastGame=game.Game()
        scores = []
        lost=False
        after = [0,0,0]
        freq = [0,0,0,0,0]
        frames=0
        while not lost:
            inpScores=[0,0,0,0,0]
            for i in range(5):
                inTest = [j==i for j in range(5)]
                inpScores[i]=model.predict([[[game.getGameState(lastGame)+inTest]]])
            move = inpScores.index(max(inpScores))
            freq[move]+=1
            if frames%300==1:
                print([i/frames for i in freq])
            moves = [i==move for i in range(5)]
            scores += [0]
            after = game.tryUpdate(lastGame,moves)
            games += [[game.getGameState(lastGame),moves]]
            lastGame=after[0]
            frames+=1
            if after[1] or after[2]:
                pt = after[1] - 20*after[2]
                for i in range(len(scores)):
                    scores[-1-i] += pt*gamma**i
            if after[2]:
                lost=True
        print(sum(scores)/len(scores))
        model.fit([[[games[i][0]+games[i][1]] for i in range(len(games))]],[[[i] for i in scores]], epochs=50)
