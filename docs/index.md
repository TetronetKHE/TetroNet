# What is TetroNet?
TetroNet is an AI that can play a tetromino falling block game. Or... maybe it can? With enough training?

# Who made it?
Team TetroNet made it, for Kent Hack Enough 2019, a hackathon in the humble city of Kent, Ohio!

## Okay, I appreciate the cool "Team %PROJECT_NAME%" thingy, but **who** made it?
* Avery - Built cube
* Chandler - 🎵🎵🎵🎵
* Kiersten - Team manager, initial concept
* Nathan - Did AI programming, bug fixes
* Vonn - Did game programming, bug fixes
* AI - Playtesting, existing in several different states

# How do I install and run it?
* You must have a 64-bit version of Python!

1. You first need an installation of Python 3.7
2. Then install PyGame by running `python -m pip install -U pygame --user`.
3. After that, install NumPy by running `python -m pip install numpy`.
4. Don't forget to install Keras! `python -m pip install keras`
5. Finally, install Tensorflow. This'll take a bit. `python -m pip install tensorflow`

Then just run `tetroNet.py`, and watch the AI fail over and over again!

## What are all these other files for?
* `game.py` is the game portion of TetroNet, run it and play a bit of Tetris!
* `ai.py` is the AI portion of TetroNet. Run it, select a backup, and it'll play game after game! (This does not train the AI.)
* All the `evaluation` files are different scoring algorithms. Eventually we'll clean things up.
