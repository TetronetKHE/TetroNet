import evaluationBMin as evaluation
import ai

aiInst = ai.AI(strategy=0, saveFileName="tetroNetBackupBMin")
aiInst.train(saves=500, steps=50, gamma=.87, tryhard=.1, evaluation=evaluation)
