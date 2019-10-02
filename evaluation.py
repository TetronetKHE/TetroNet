import game
import random

random.seed(1984)

def train(model, steps, gamma):
	games = []
	scores = []
	for step in range(steps):
		print(f"Step #{step}") # print progress
		
		lastGame = game.Game()
		
		freq = [0 for i in range(game.InputLength)]
		
		# Temporary variables
		score = 0
		frames = 0
		
		while True:
			inpScores=[0 for i in range(game.InputLength)] # Fitness scores of each inputs
			
			for i in range(game.InputLength):
				inTest = [j==i for j in range(game.InputLength)]
				inpScores[i] = model.predict([[[lastGame.getState() + inTest]]])
			
			move = inpScores.index(max(inpScores))
			if random.random()>.9: # Tryhard algorithm
				move = random.randint(0,5)
			freq[move]+=1
			moves = [i==move for i in range(game.InputLength)]
			
			frames += 1
			
			scores += [0]
			
			after = lastGame.tryUpdate(moves) # Get next states
			games += [[lastGame.getState(), moves]]
			
			lastGame = after[0]
			if after[1] or after[2] or after[3] or after[4]:
				pt = 5 * after[1] ** 1.2 - 100 * after[2] - 3 * after[3] + 2 * after[4]
				score += pt
				for i in range(frames):
					scores[-1-i] += pt * gamma ** i
					
			if lastGame.gameOver: break
		print(round(score / frames, 2), frames, [round(i/frames, 4) for i in freq])
		
		# AI magic
		model.fit([[[games[i][0] + games[i][1]] for i in range(len(games))]], [[[i] for i in scores]], epochs=100, verbose=0)
	
	playAIGame(model)

def playAIGame(model):
	gwindow = game.GameWindow()
	ggame = game.Game()
	
	while True:
		gwindow.updateEvents()
		
		# if gwindow.everyXFrames(20):
		inpScores=[0 for i in range(game.InputLength)]
		
		for i in range(game.InputLength):
			inTest = [j==i for j in range(game.InputLength)]
			inpScores[i] = model.predict([[[ggame.getState() + inTest]]])
		
		move = inpScores.index(max(inpScores))
		moves = [i==move for i in range(game.InputLength)]
		
		ggame.update(moves)
		if gwindow.shouldStop(ggame): break
		
		gwindow.drawGame(ggame)
		
	gwindow.close()
	gwindow = None
