import random

patientAge = 34
waitingTime = 0
weight = 62
cr=random.uniform (1.2,20)
gfr = ((140-patientAge)*weight)/(72*cr)
print (gfr)
score = -2*gfr+(100-patientAge) + 0.1*(waitingTime)
print (score)