import evaluationMore as evaluation
import ai

aiInst = ai.AI(strategy=0, saveFileName="tetroNetBackupDN")
aiInst.train(saves=200, steps=50, gamma=.88, tryhard=.0001, evaluation=evaluation)
