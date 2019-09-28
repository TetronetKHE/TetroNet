#import numpy as np
from evaluation import train

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

model = Sequential()
model.add(Flatten(input_shape=(1,221)))
model.add(Dense(120))
model.add(Dense(1))
model.add(Activation('linear'))
model.compile('adam','mean_squared_error')
print(model.summary())

for i in range(1000):
    train(model,10,.92)
    model.save("tetroNetBackup")
    print("Saved")
