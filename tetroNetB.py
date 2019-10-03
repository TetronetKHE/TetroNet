#import numpy as np
from evaluationB import train

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.optimizers import Adam

model = Sequential()
model.add(Flatten(input_shape=(1,222)))
model.add(Dense(280,activation="relu"))
model.add(Dense(220,activation="relu"))
model.add(Dense(120,activation="relu"))
model.add(Dense(1))
model.add(Activation('linear'))
model.compile('adam','mean_absolute_error')
try:
    model.load_weights("tetroNetBackupB")
except:
    print("failed")
print(model.summary())

saves=300
gamma=.87
tryhard=.99

for i in range(saves):
    train(model,int(100000/saves),gamma,tryhard)
    model.save_weights("tetroNetBackupB")
    print(str(i/saves)+"Saved")
