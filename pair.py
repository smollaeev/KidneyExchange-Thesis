import pandas as pd
import numpy as np
import random
import array
from donor import Donor
from patient import Patient

class Pair:
    def __init__(self, patient, donor):
        self.patient=patient
        self.donor=donor
    
    def BloodType_match (self):
        if (self.patient.bloodType == self.donor.bloodType) or (self.donor.bloodType == "o"):
            return True
        else:
            if (self.patient.bloodType == "ab") and ((self.donor.bloodType == "a") or (self.donor.bloodType == "b")):
                return True
            else:
                return False

    def calculate_AgeDifference (self):
        self.ageDifference = self.donor.age - self.patient.age

    def get_Fitness (self):
        incompatibilityPenalty = -400000
        compatibilityPrize = 5000
        ageDifferencePenalty = -0.2
        # marketDonorPenalty = -3000
        if self.BloodType_match ():
            self.goodnessOfMatch = compatibilityPrize
        else:
            self.goodnessOfMatch = incompatibilityPenalty

        self.calculate_AgeDifference ()
        if self.ageDifference > 0:
            self.goodnessOfMatch += (self.ageDifference*ageDifferencePenalty)
        # if (self.donor.type == 'IncompatibleMarketDonor') or (self.donor.type == 'market'):
        #     self.goodnessOfMatch += marketDonorPenalty
        
        return self.goodnessOfMatch