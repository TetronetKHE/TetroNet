import evaluationB as evaluation
import ai

aiInst = ai.AI(strategy=1, saveFileName="tetroNetBackupB")
aiInst.train(saves=2500, steps=2, gamma=.99, tryhard=0.01,epochs=1, freq=10, evaluation=evaluation)
