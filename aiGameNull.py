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

while True:
        
        frame = 0
        game = Game()
        inputs = [0, 0, 0, 0, 0]
        screen = startWindow()
        while True:
                inpScores=[0,0,0,0,0] #fitness scores of each inputs
                for i in range(5):
                        inTest = [j==i for j in range(5)]
                        inpScores[i]=model.predict([[[getGameState(game)+inTest]]])
                move = inpScores.index(max(inpScores))
                inputs = [i==move for i in range(5)]
                if frame % 60 == 0:
                        game.update(inputs)
                        print(inputs)
                if game.gameOver: break
                
                drawGame(game, screen)
                frame += 1
        
        closeWindow()
