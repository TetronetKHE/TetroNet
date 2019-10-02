import numpy as np
import game
import random

random.seed(1984)

def train(model, steps, gamma, show=False):
    games=[]
    scores=[]
    for step in range(steps):
		# Print step progress
        print("step " + str(step))
		
		
        lastGame=game.Game()
        lost=False
        after = [0,0,0]
        freq = [0,0,0,0,0,0]
        score=0
        frames=0
        while not lost:
            inpScores=[0,0,0,0,0,0] #fitness scores of each inputs
            for i in range(6):
                inTest = [j==i for j in range(6)]
                inpScores[i]=model.predict([[[game.getState(lastGame)+inTest]]])
            move = inpScores.index(max(inpScores)) #find largest fitness
            freq[move]+=1
            frames+=1
            if frames%300==30:
                print(frames/60)
            moves = [i==move for i in range(6)]
            if random.random()>.9:                 #Tryhard algorithm
                r = random.randint(0,5)
                moves = [i==r for i in range(6)]
            scores += [0]
            after = game.tryUpdate(lastGame,moves[:-1])  #get next states
            games += [[game.getState(lastGame),moves]]
            lastGame=after[0]
            if after[1]:
                print("LINEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE" + str(after[1]))
            if after[2] or after[4]:
                pt = after[4]-50*after[2]
                score+=pt
                for i in range(frames):
                    scores[-1-i] += pt*gamma**i
            if after[2]:
                lost=True
        print(score/frames, [i/frames for i in freq], frames)
        model.fit([[[games[i][0]+games[i][1]] for i in range(len(games))]],[[[i] for i in scores]], epochs=100, verbose=0)
    lost=False
    ggame = game.Game()
    gameVisual = game.startWindow()
    while not lost:
        inpScores=[0,0,0,0,0,0]
        game.drawGame(ggame,gameVisual)
        for i in range(6):
            inTest = [j==i for j in range(6)]
            inpScores[i] = model.predict([[[game.getState(ggame)+inTest]]])
        move = inpScores.index(max(inpScores))
        moves = [i==move for i in range(5)]
        after = game.tryUpdate(ggame, moves)
        ggame=after[0]
        if after[1]:
            print("LINEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"+str(after[1]))
        lost = after[2]
    game.closeWindow()
    print("Sim end")
