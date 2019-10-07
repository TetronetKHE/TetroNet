import evaluation
import ai

aiInst = ai.AI(strategy=0, saveFileName="tetroNetBackup")
aiInst.train(saves=300, steps=50, gamma=.87, tryhard=.1, evaluation=evaluation)
