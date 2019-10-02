def setUpAI(saveFileName = None):
	model = Sequential()
	model.add(Flatten(input_shape=(1,221)))
	model.add(Dense(180,activation="relu"))
	model.add(Dense(120,activation="relu"))
	model.add(Dense(1))
	model.add(Activation('linear'))
	model.compile('adam','mean_absolute_error')
	if saveFileName: try: model.load_weights(saveFileName)
