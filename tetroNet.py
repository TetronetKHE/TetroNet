import numpy as np
import train from evaluation.py

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

model = Sequential()
model.add(Flatten(input_shape=(1,212)))
model.add(Dense(30))
model.add(Dense(1))
model.add(Activation('linear'))
print(model.summary())

for i in range(2000):
    train(model,5,.99)
    model.save("tetroNetBackup")
