import numpy as np
import game
import random

random.seed(1984)

def train(model, steps, gamma, show=False):
	games=[]
	scores=[]
	for step in range(steps):
		print("step " + str(step))#print progress
		lastGame=game.Game()
		lost=False
		after = [0,0,0]
		freq = [0 for i in range(game.InputLength)]
		score=0
		frames=0
		while not lost:
			inpScores=[0 for i in range(game.InputLength)] #fitness scores of each inputs
			for i in range(5):
				inTest = [j==i for j in range(game.InputLength)]
				inpScores[i]=model.predict([[[lastGame.getState()+inTest]]])
			move = inpScores.index(max(inpScores)) #find largest fitness
			freq[move]+=1
			frames+=1
			if frames%300==30:
				print(frames/60)
			moves = [i==move for i in range(game.InputLength)]
			if random.random()>.9:                 #Tryhard algorithm
				r = random.randint(0,5)
				moves = [i==r for i in range(game.InputLength)]
			scores += [0]
			after = lastGame.tryUpdate(moves)  #get next states
			games += [[lastGame.getState(),moves]]
			lastGame=after[0]
			if after[1]:
				print("LINEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE" + str(after[1]))
			if after[1] or after[2] or after[3] or after[4]:
				pt = 5*after[1]**1.2-100*after[2]-3*after[3]+2*after[4]
				score+=pt
				for i in range(frames):
					scores[-1-i] += pt*gamma**i
			if after[2]:
				lost=True
		print(score/frames, [i/frames for i in freq], frames)
		model.fit([[[games[i][0]+games[i][1]] for i in range(len(games))]],[[[i] for i in scores]], epochs=100, verbose=0)
	
	gwindow = game.GameWindow()
	ggame = game.Game()
	
	while True:
		gwindow.updateEvents()
		
		# if gwindow.everyXFrames(20):
		inpScores=[0 for i in range(game.InputLength)]
		
		for i in range(6):
			inTest = [j==i for j in range(game.InputLength)]
			inpScores[i] = model.predict([[[ggame.getState() + inTest]]])
		
		move = inpScores.index(max(inpScores))
		moves = [i==move for i in range(game.InputLength)]
		
		ggame.update(moves)
		if gwindow.shouldStop(ggame): break
		
		gwindow.drawGame(ggame)
		
	gwindow.close()
