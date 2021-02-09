from names import get_full_name
import random
import datetime
import pandas as pd
import numpy as np
import array

class Patient:

    def __init__ (self, name, type, age, weight, bloodType, probabilityOfRejection, alcohol, smoke, disease, donor, waitingTime, gfr, score):

        self.name=name
        self.type = type
        self.age=age
        self.weight= weight
        self.bloodType=bloodType
        self.probabilityofRejection=probabilityOfRejection
        self.alcohol=alcohol
        self.smoke=smoke
        # self.drug=drug
        self.disease=disease
        self.donor=donor
        self.waitingTime = waitingTime
        self.gfr = gfr
        self.score = score
        self.priority = 0
        self.qualityoflifeIndex = 3

    def determine_QualityOfLife (self):
        if self.alcohol == 1:
            self.qualityoflifeIndex -= 1
        if self.smoke == 1:
            self.qualityoflifeIndex -= 1
        # if self.drug == 1:
        #     self.qualityoflifeIndex -= 1 
        if self.disease == 1:
            self.qualityoflifeIndex -= 1

    def __classifyby_QualityOfLife (self, priority1, priority2, priority3, priority4):
        # if self.qualityoflifeIndex == 4:
        #     priority1.append (self.score)
        if self.qualityoflifeIndex == 3:
            priority1.append (self.score)
        if self.qualityoflifeIndex == 2:
            priority2.append (self.score)
        if self.qualityoflifeIndex == 1:
            priority3.append (self.score)
        if self.qualityoflifeIndex == 0:
            priority4.append (self.score)
        return priority1, priority2, priority3, priority4

    @staticmethod
    def determine_Priority (patients):  
        priority1 = []
        priority2 = []
        priority3 = []
        priority4 = []  
        # priority5 = []

        for patient in patients:
            patient.determine_QualityOfLife()
        
        for patient in patients:
            if patient.type == "waitlist":
                priority1, priority2, priority3, priority4 = patient.__classifyby_QualityOfLife (priority1, priority2, priority3, priority4)

        priority1.sort (reverse = True)
        priority2.sort (reverse = True)
        priority3.sort (reverse = True)
        priority4.sort (reverse = True)
        # priority5.sort (reverse = True)
        p=0
        for i in range(len(priority1)):
            for patient in patients:
                if priority1[i] == patient.score:
                    patient.priority = i+1
        try:
            p=i+1
        except:
            p=0
        for i in range(0,len(priority2)):
            p+=1
            for patient in patients:
                if priority2[i] == patient.score:
                    patient.priority = p
                    
        for i in range(0,len(priority3)):
            p+=1
            for patient in patients:
                if priority3[i] == patient.score:
                    patient.priority = p

        for i in range(0,len(priority4)):
            p+=1
            for patient in patients:
                if priority4[i] == patient.score:
                    patient.priority = p

        # for i in range(0,len(priority5)):
        #     p+=1
        #     for patient in patients:
        #         if priority5[i] == patient.score:
        #             patient.priority = p