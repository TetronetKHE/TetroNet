import game

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.optimizers import Adam

model = Sequential()
model.add(Flatten(input_shape=(1,221)))
model.add(Dense(180,activation="relu"))
model.add(Dense(120,activation="relu"))
model.add(Dense(1))
model.add(Activation('linear'))
model.compile('adam','mean_absolute_error')
model.load_weights('tetroNetBackup')

gwindow = game.GameWindow()
gwindow.cueTheMusic()

while True:
	gameInst = game.Game()
	
	while True:
		# Reset scores.
		inputScores = [0 for i in range(game.InputLength)]
		
		# Do AI magic (TODO: what does this mean?)
		for i in range(game.InputLength):
			inTest = [j==i for j in range(game.InputLength)]
			inputScores[i] = model.predict( [[[getGameState(game) + inTest]]] )
		move = inputScores.index(max(inputScores))
		inputs = [i == move for i in range(game.InputLength)]
			game.update(inputs)
			print(inputs)
		if game.gameOver: break
		
		drawGame(game, screen)
	
	closeWindow()

gwindow = GameWindow(True)
gwindow.cueTheMusic()

game = Game()

while True:
	gwindow.updateEvents()
	if gwindow.everyXFrames(20):
		# ADD AI CODE HERE
		print(game.tryUpdate(gwindow.inputs))
		game.update(gwindow.inputs)
		# END AI CODE
		if gwindow.shouldStop(game): break
	gwindow.drawGame(game)

gwindow.close()
sys.exit()
