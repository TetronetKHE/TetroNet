from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.optimizers import Adam

import game

class AI:
	PlaySpeed = 1
	SaveDirectory = "backups\\"
	
	def __init__(self, strategy = 0, saveFileName = None):
		self.model = Sequential()
		self.model.add(Flatten(input_shape=(1,222)))
		if strategy == 0:
			self.model.add(Dense(180, activation="relu"))
			self.model.add(Dense(120, activation="relu"))
			self.model.add(Dense(1))
		elif strategy == 1:
			self.model.add(Dense(280, activation="relu"))
			self.model.add(Dense(220, activation="relu"))
			self.model.add(Dense(120, activation="relu"))
			self.model.add(Dense(1))
		self.model.add(Activation("linear"))
		self.model.compile("adam", "mean_absolute_error")
		
		if saveFileName:
			try:
				self.model.load_weights(AI.SaveDirectory + saveFileName)
				print("== Loaded weights from backup. ==")
			except:
				print('8888888888 8888888b.  8888888b.   .d88888b.  8888888b.  888')
				print('888        888   Y88b 888   Y88b d88P" "Y88b 888   Y88b 888')
				print('888        888    888 888    888 888     888 888    888 888')
				print('8888888    888   d88P 888   d88P 888     888 888   d88P 888')
				print('888        8888888P"  8888888P"  888     888 8888888P"  888')
				print('888        888 T88b   888 T88b   888     888 888 T88b   Y8P')
				print('888        888  T88b  888  T88b  Y88b. .d88P 888  T88b   " ')
				print('8888888888 888   T88b 888   T88b  "Y88888P"  888   T88b 888')
				print(f"== Could not load backup with name {saveFileName}! ==")
				print("== If this is the first time running TetroNet, that's okay! ==")
				print("== Otherwise, that's pretty bad. See if it got corrupted. ==")
		else:
			print('888       888        d8888 8888888b.  888b    888 8888888 888b    888  .d8888b.  888')
			print('888   o   888       d88888 888   Y88b 8888b   888   888   8888b   888 d88P""Y88b 888')
			print('888  d8b  888      d88P888 888    888 88888b  888   888   88888b  888 888    888 888')
			print('888 d888b 888     d88P 888 888   d88P 888Y88b 888   888   888Y88b 888 888        888')
			print('888d88888b888    d88P  888 8888888P"  888 Y88b888   888   888 Y88b888 888  88888 888')
			print('88888P Y88888   d88P   888 888 T88b   888  Y88888   888   888  Y88888 888    888 Y8P')
			print('8888P   Y8888  d8888888888 888  T88b  888   Y8888   888   888   Y8888 Y88b..d88P  " ')
			print('888P     Y888 d88P     888 888   T88b 888    Y888 8888888 888    Y888  "Y8888P88 888')
			print("== No backup file name assigned! ==")
			saveFileName = "untitledBackup1"
		self.saveFileName = saveFileName
		
		print(self.model.summary())
	
	def saveWeights(self):
		self.model.save_weights(AI.SaveDirectory + self.saveFileName)
	
	def train(self, saves=300, steps=50, gamma=.99, tryhard=.03, evaluation=None):
		if not evaluation:
			import evaluation
		
		for saveStep in range(saves):
			evaluation.train(self.model, steps, gamma, tryhard)
			self.saveWeights()
			print(f"== Saved weights to backup file. {saveStep}/{saves} complete. ==")
			self.playGames()
	
	def playGames(self, forever=False, music=False):
		gameWindow = game.GameWindow()
		if music: gameWindow.cueTheMusic()

		while True:
			gameInst = game.Game()
			
			while True:
				gameWindow.updateEvents()
				if gameWindow.everyXFrames(AI.PlaySpeed):
					# Reset scores.
					inputScores = [0 for i in range(game.InputLength)]
					
					# Do AI magic
					for i in range(game.InputLength):
						inputs = [j==i for j in range(game.InputLength)]
						inputScores[i] = self.model.predict([[[gameInst.getState() + inputs]]])
					
					# Decide input (gets the input with the highest score)
					move = inputScores.index(max(inputScores))
					
					# Set inputs
					inputs = [i == move for i in range(game.InputLength)]
					# print(inputs)
					
					# Update game with decision.
					gameInst.update(inputs)
				if gameWindow.shouldStop(gameInst): break
				
				gameWindow.drawGame(gameInst)
			
			if gameWindow.stop or not forever: break

		gameWindow.close()

if __name__ == "__main__":
	strategy = int(input("Enter strategy (0 for old, 1 for new.)"))
	backupName = input(f"Enter rest of filename: {AI.SaveDirectory}tetroNetBackup")
	if backupName != "None": # (Yes, I mean "None" and not None)
		aiInst = AI(strategy=strategy, saveFileName=f'tetroNetBackup{backupName}')
	else:
		aiInst = AI(strategy=strategy)
	aiInst.playGames(forever=True)
