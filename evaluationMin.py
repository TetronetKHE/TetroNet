import game
import random

def train(model, steps, gamma, tryhard=0.1):
	games = []
	scores = []
	for step in range(steps):
		# Print step progress
		print(f"Step {step} of {steps}")
		
		lastGame = game.Game()
		
		freq = [0 for i in range(game.InputLength)]
		
		# Temporary variables
		score = 0
		frames = 0
		
		while True:
			# Fitness scores of each input
			inputScores = [0 for i in range(game.InputLength)]
			
			for i in range(game.InputLength):
				inTest = [j==i for j in range(game.InputLength)]
				inputScores[i] = model.predict([[[lastGame.getState() + inTest]]])
			
			move = inputScores.index(max(inputScores))
			if random.random() < tryhard: # Tryhard algorithm
				move = random.randint(0, game.InputLength)
			freq[move]+=1
			moves = [i==move for i in range(game.InputLength)]
			
			frames += 1
			
			scores.append(0)
			
			after = lastGame.tryUpdate(moves) # Get next states
			games += [[lastGame.getState(), moves]]
			
			lastGame = after[0]
			if after[1] or after[2] or after[3] or after[4]:
				pt = after[4]
				score += pt
				for i in range(frames):
					scores[-1-i] += pt * gamma ** i
					
			if lastGame.gameOver: break
		print(round(score / frames, 2), frames, [round(i/frames, 4) for i in freq])
	# AI magic
	model.fit([[[games[i][0] + games[i][1]] for i in range(len(games))]], [[[i] for i in scores]], epochs=100, verbose=0)
