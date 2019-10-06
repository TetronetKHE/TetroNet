import evaluationB as evaluation
import ai

aiInst = ai.AI(strategy=1, saveFileName="tetroNetBackupB")
aiInst.train(saves=300, steps=50, gamma=.99, tryhard=0.01,epochs=5, evaluation=evaluation)
