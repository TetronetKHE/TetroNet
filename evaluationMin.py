import numpy as np
import game
import random

random.seed(1984)

def train(model, steps, gamma, show=False):
    games=[]
    scores=[]
    for asdfghjkl in range(steps):
        print("step " + str(asdfghjkl))#print progress
        lastGame=game.Game()
        lost=False
        after = [0,0,0]
        freq = [0,0,0,0,0]
        frames=0
        while not lost:
            inpScores=[0,0,0,0,0] #fitness scores of each inputs
            for i in range(5):
                inTest = [j==i for j in range(5)]
                inpScores[i]=model.predict([[[game.getGameState(lastGame)+inTest]]])
            move = inpScores.index(max(inpScores)) #find largest fitness
            freq[move]+=1
            frames+=1
            if frames%300==30:
                print(frames/60, [i/frames for i in freq])
            moves = [i==move for i in range(5)]
            if random.random()>.55:                 #Tryhard algorithm
                r = random.randint(0,4)
                moves = [i==r for i in range(5)]
            scores += [0]
            after = game.tryUpdate(lastGame,moves)  #get next states
            games += [[game.getGameState(lastGame),moves]]
            lastGame=after[0]
            if after[1]:
                print("LINEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            if after[1] or after[2] or after[3] or after[4]:
                pt = after[4]
                for i in range(len(scores)):
                    scores[-1-i] += pt*gamma**i
            if after[2]:
                lost=True
        print(sum(scores)/len(scores), [i/frames for i in freq], frames/60)
        model.fit([[[games[i][0]+games[i][1]] for i in range(len(games))]],[[[i] for i in scores]], epochs=100, verbose=0)
        lost=False
        ggame = game.Game()
        gameVisual = game.startWindow()
        while not lost:
            inpScores=[0,0,0,0,0]
            game.drawGame(ggame,gameVisual)
            for i in range(5):
                inTest = [j==i for j in range(5)]
                inpScores[i]=model.predict([[[game.getGameState(ggame)+inTest]]])
            move = inpScores.index(max(inpScores))
            moves = [i==move for i in range(5)]
            after = game.tryUpdate(ggame, moves)
            ggame=after[0]
            if after[1]:
                print("LINEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            lost = after[2]
        game.closeWindow()
        print("Sim end")