import evaluationMoreMin as evaluation
import ai

aiInst = ai.AI(strategy=0, saveFileName="tetroNetBackupDNMin")
aiInst.train(saves=500, steps=20, gamma=.88, tryhard=.1, evaluation=evaluation)
