#import numpy as np
from evaluation import train

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

model = Sequential()
model.add(Flatten(input_shape=(1,212)))
model.add(Dense(30))
model.add(Dense(1))
model.add(Activation('linear'))
model.compile('adam','mean_squared_error')
print(model.summary())

for i in range(2000):
    train(model,5,.85)
    model.save("tetroNetBackup")
    print("Saved")
