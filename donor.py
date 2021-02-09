import pandas as pd
import numpy as np
import random
import datetime
import array

class Donor:
    def __init__(self, name, gender, age, patientName, type, bloodType):
        self.name = name
        self.gender = gender
        self.age = age
        self.patientName=patientName
        self.type=type
        self.bloodType = bloodType
