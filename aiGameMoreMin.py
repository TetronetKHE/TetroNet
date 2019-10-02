import game

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.optimizers import Adam

model = Sequential()
model.add(Flatten(input_shape=(1,222)))
model.add(Dense(180,activation="relu"))
model.add(Dense(120,activation="relu"))
model.add(Dense(1))
model.add(Activation('linear'))
model.compile('adam','mean_absolute_error')
model.load_weights('tetroNetBackupDNMin')

pygame.mixer.init()
pygame.mixer.music.load('resources\\Tetris.ogg')
pygame.mixer.music.play(-1)

while True:
        screen = startWindow()
        
        frame = 0
        game = Game()
        inputs = [0, 0, 0, 0, 0]
        
        while True:
                inpScores=[0,0,0,0,0,0] #fitness scores of each inputs
                for i in range(6):
                        inTest = [j==i for j in range(6)]
                        inpScores[i]=model.predict([[[getGameState(game)+inTest]]])
                move = inpScores.index(max(inpScores))
                inputs = [i==move for i in range(5)]
                if frame % 20 == 0:
                        game.update(inputs)
                        print(inputs)
                if game.gameOver: break
                
                drawGame(game, screen)
                frame += 1
        
        closeWindow()
