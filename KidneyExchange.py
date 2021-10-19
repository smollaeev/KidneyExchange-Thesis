from Repository import Repository
from solution import Solution
from patient import Patient

#Go to class Solution, class Population & class Chromosome to change Genetic Algorithm parameters  

def main():   
    for i in range (3):
        R = Repository()
        patients, donors = R.get_Data ()

        Patient.determine_Priority (patients)

        

        solution = Solution (patients, donors)

    
        solution.GeneticAlgorithm ()
        solution.show_Results (i)

if __name__ == "__main__":
    main ()  