#import numpy as np
from evaluationMore import train

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
try:
    model.load_weights("tetroNetBackup")
except:
    print("failed")
print(model.summary())

for i in range(500):
    train(model,20,.88)
    model.save_weights("tetroNetBackupDN")
    print(str(i/500)+"Saved")
