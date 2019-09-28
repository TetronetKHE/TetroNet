import numpy as np
#import game

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

model = Sequential()
model.add(Flatten(input_shape=(1,204)))
model.add(Dense(30))
model.add(Dense(7))
model.add(Activation('linear'))
print(model.summary())
