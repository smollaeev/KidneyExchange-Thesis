from names import get_full_name
import random
import datetime
import pandas as pd
import numpy as np
import array
import jsonpickle
import copy

from patient import Patient
from donor import Donor 


def BloodTypeCompatibile(patient,bloodType):
    if (bloodType == patient.bloodType) or (bloodType == "o"):
        return True
    else:
        if (patient.bloodType == "ab") and ((bloodType == "a") or (bloodType == "b")):
            return True
    return False

def incomp_BloodType (patient,p_blood_typ_com,blood_typ_sort):
    bloodType=patient.bloodType
    while BloodTypeCompatibile(patient,bloodType):
        p_rand=random.uniform(0,1)
        for i in range(0,4):
            if p_rand<=p_blood_typ_com[i]:
                rand_blood_typ_number=random.randint(i,3)
                bloodType=blood_typ_sort[rand_blood_typ_number]
                break
    return bloodType

def determine_PatientBloodType (commulatedprobabilityofBloodTypes, sortedBloodType):
    p_rand = random.uniform(0,1)
    for i in range(0,4):
        if p_rand <= commulatedprobabilityofBloodTypes [i]:
            rand_blood_typ_number = random.randint (i,3)
            patientBloodType = sortedBloodType [rand_blood_typ_number]
            break 
    return patientBloodType


def create_PatientData (type, probabilityofFemalePatient = 0.409, probabilityofAgeUnder45 = 0.7, sortedBloodType = ['ab','b','a','o'],
                        probabilityofBloodTypes = [0.3,0.24,0.08,0.38], sortedPRALevels = ['high','med','low'],
                        probabilityofPRALevels = [0.7019, 0.2, 0.0981], probabilityofIncompatibility = {'low':0.05,'med':0.1,'high':0.9},
                        probabilityofIncompatibleRelativeDonor = 0.05):

    
    sortedprobabilityofBloodTypes = probabilityofBloodTypes         
    sortedprobabilityofBloodTypes.sort()
    commulatedprobabilityofBloodTypes = sortedprobabilityofBloodTypes
    for i in range (1,4):
        commulatedprobabilityofBloodTypes [i] += commulatedprobabilityofBloodTypes [i-1]

    sortedprobabilityofPRALevels = probabilityofPRALevels
    sortedprobabilityofPRALevels.sort()
    commulatedprobabilityofPRALevels = sortedprobabilityofPRALevels
    for i in range (1,3):
        commulatedprobabilityofPRALevels [i] += commulatedprobabilityofPRALevels [i-1]

    patientType = type

    # determining the name and gender of the patient
    p_rand = random.uniform(0,1)
    if p_rand <= probabilityofFemalePatient:
        patientGender = 'f'
        patientName = get_full_name ('female')
    else:
        patientGender = 'm'
        patientName = get_full_name('male')

    #determining the birth year and age of the patient
    p_rand = random.uniform (0,1)
    date = datetime.date.today ()
    if p_rand < probabilityofAgeUnder45:
        start_date = datetime.date (date.year-44, 1,1)
        end_date = datetime.date (date.year-19,1,1)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange (days_between_dates)
        patient_birth_date = start_date + datetime.timedelta (days=random_number_of_days)
        patientAge = date.year-patient_birth_date.year
    else:
        start_date = datetime.date (date.year-70, 1,1)
        end_date = datetime.date (date.year-44, 1,1)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange (days_between_dates)
        patient_birth_date = start_date + datetime.timedelta (days=random_number_of_days)
        patientAge = date.year - patient_birth_date.year
    
    #determining weight and registeration date of the patient
    weight = random.randint(50,120)

    if type == 'waitlist':            
        start_date = datetime.date (random.randint(date.year-2,date.year), 1,1)
        time_between_dates = date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        reg_date = start_date + datetime.timedelta(days=random_number_of_days)
        waitingTime = (date-reg_date).days
    
    else:
        waitingTime = None   

    #determining blood type
    if patientType == "incomp_patient":
        patientBloodType = 'ab'
        while patientBloodType == 'ab':
            patientBloodType = determine_PatientBloodType (commulatedprobabilityofBloodTypes, sortedBloodType)
    else:
        patientBloodType = determine_PatientBloodType (commulatedprobabilityofBloodTypes, sortedBloodType)  

    #PRA Level and probability of incompatibility based on PRA Level
    p_rand = random.uniform(0,1)
    for i in range(0,3):
        if p_rand <= commulatedprobabilityofPRALevels [i]:
            rand_pra_number = random.randint (i,2)
            pra = sortedPRALevels [rand_pra_number]
            break   

    probabilityofRejection = probabilityofIncompatibility [pra]

    #Creatinine Level and GFR
    if patientType == 'waitlist':
        if patientGender == 'f':
            cr = random.uniform (1.2,20)
            gfr = ((140-patientAge)*weight*0.85)/(72*cr)
            score = -2*gfr+(100-patientAge) + 0.1*(waitingTime)
        if patientGender=='m':
            cr=random.uniform (1.4,20)
            gfr = ((140-patientAge)*weight)/(72*cr)
            score = -2*gfr+(100-patientAge) + 0.1*(waitingTime)

    else:
        gfr = None
        score = None           

    #life style
    alcohol = random.randint(0,1)
    smoke = random.randint(0,1)
    # drug = random.randint(0,1)
    disease = random.randint(0,1)

    patientDonor = Donor('','',0,'','','')

    patient = Patient(patientName, type, patientAge, weight, patientBloodType, probabilityofRejection, alcohol, smoke, disease,
                        patientDonor, waitingTime, gfr, score)

    # incomp_donor
    if type == "incomp_patient":
        p_rand = random.uniform(0,1)
        if p_rand < probabilityofIncompatibleRelativeDonor:
            patient.donor = CreateDonorData ("IncompatibleRelativeDonor", patient=patient)
        else:
            patient.donor = CreateDonorData ("IncompatibleMarketDonor", patient=patient)
            
    return patient

def CreateDonorData(DonorType, patient=None, blood_typ_sort = ['ab','b','a','o'], 
                    p_blood_typ = [0.3,0.24,0.08,0.38], p_market_Age2526=0.5):

    p_blood_typ_sort = copy.deepcopy(p_blood_typ)              
    p_blood_typ_sort.sort()
    p_blood_typ_com = copy.deepcopy(p_blood_typ_sort)
    for i in range(1,4):
        p_blood_typ_com[i] += p_blood_typ_com [i-1]

    if patient:
        donor_PatientName = patient.name
    else:
        donor_PatientName = ''

    if DonorType == "market"or DonorType == "IncompatibleMarketDonor":
        donor_p_female = 0.1
    elif DonorType == "deceased":
        donor_p_female = 0.5
    elif DonorType == "IncompatibleRelativeDonor":
        donor_p_female = 0.625

    # determining the name and gender of the donor
    p_rand = random.uniform(0,1)
    if p_rand <= donor_p_female:
        donor_gender = 'f'
        donor_name = get_full_name('female')
    else:
        donor_gender = 'm'
        donor_name = get_full_name('male')

    #birth date and age
    p_rand=random.uniform(0,1)
    date=datetime.date.today()
    if DonorType=="market"or DonorType=="IncompatibleMarketDonor":
        if p_rand<p_market_Age2526:
            start_date=datetime.date(date.year-26, 1,1)
            end_date=datetime.date(date.year-24, 1,1)
            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_number_of_days = random.randrange(days_between_dates)
            donor_birth_date = start_date + datetime.timedelta(days=random_number_of_days)
            donor_age=date.year-donor_birth_date.year
        else:
            start_date=datetime.date(date.year-35, 1,1)
            end_date=datetime.date(date.year-17, 1,1)
            time_between_dates = end_date - start_date
            days_between_dates = time_between_dates.days
            random_number_of_days = random.randrange(days_between_dates)
            donor_birth_date = start_date + datetime.timedelta(days=random_number_of_days)
            donor_age=date.year-donor_birth_date.year

    if DonorType=="IncompatibleRelativeDonor":
        donor_birth_date=datetime.date(int(np.random.normal(date.year-41,4)), 1,1)
        donor_age=date.year-donor_birth_date.year

    if DonorType=="deceased":
        start_date=datetime.date(date.year-35, 1,1)
        end_date=datetime.date(date.year-17, 1,1)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        donor_birth_date = start_date + datetime.timedelta(days=random_number_of_days)
        donor_age=date.year-donor_birth_date.year

    #determining blood type
    if DonorType=="IncompatibleRelativeDonor" or DonorType=="IncompatibleMarketDonor":
        donor_BloodType = incomp_BloodType(patient, p_blood_typ_com, blood_typ_sort)

    else:
        p_rand=random.uniform(0,1)
        for i in range(0,4):
            if p_rand<=p_blood_typ_com[i]:
                rand_blood_typ_number=random.randint(i,3)
                break
        donor_BloodType = blood_typ_sort[rand_blood_typ_number]

    donor = Donor(donor_name, donor_gender, donor_age, donor_PatientName, DonorType, donor_BloodType) 
    return donor

def main():
    ans1=input("Do you want to create a new database? (All previous data will be replaced)(y/n)")
    if ans1=="y":

        n_WaitList=80
        n_IncompPatient=0
        n_DeceasedDonor=20
        n_Market=15
        
        patients=[]
        donors=[]

        for _ in range(n_WaitList):
            patients.append(create_PatientData('waitlist'))
        # for j in range(n_WaitList,n_IncompPatient+n_WaitList):
        #     patients.append(create_PatientData("incomp_patient"))
        #     donors.append(patients[j].donor)
        # for _ in range(n_DeceasedDonor):
        #     donors.append(CreateDonorData('deceased'))
        # for _ in range(n_Market):
        #     donors.append(CreateDonorData('market'))


        with open("PatientData - n = 10 - without incompatible.json", "w") as write_file:
            write_file.write(jsonpickle.encode(patients, indent=4))

        # with open("DonorData.json", "w") as write_file:
        #     write_file.write(jsonpickle.encode(donors, indent=4))

if __name__ == "__main__":
    main()
