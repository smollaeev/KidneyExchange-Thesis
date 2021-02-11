import jsonpickle
from patient import Patient
from donor import Donor

class Repository:    

    def __GetData_patients(self):
        with open("PatientData- n = 10.json","r") as patients_data:
            patients=jsonpickle.decode(patients_data.read())
        return patients
        
    def __GetData_donors(self):
        with open("DonorData- n = 10.json","r") as donors_data:
            donors=jsonpickle.decode(donors_data.read())
        return donors

    def get_Data (self):
        patients=self.__GetData_patients()  
        donors=self.__GetData_donors()
        return patients,donors
