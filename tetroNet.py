#import numpy as np
from evaluation import train

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
	model.load_weights("backups\\tetroNetBackup.coolFileExtension")
	print("== Loaded weights from backup. ==")
except:
	print("== Uh oh! Could not load backup! ==")
	print("== If this is the first time running TetroNet, that's okay! ==")
	print("== Otherwise, that's pretty bad! ==")
print(model.summary())

# for i in range(100):
while True:
	train(model, 20, .88)
	model.save_weights("backups\\tetroNetBackup.coolFileExtension")
	print(f"== Saved weights to backup. {i}/500 complete. ==")
