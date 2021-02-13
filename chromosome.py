import numpy as np
import random
import copy

from pair import Pair
from chain import Chain
from cycle import Cycle
from patient import Patient
from donor import Donor
from Repository import Repository

class Chromosome:

    probabilityOfRejectionPenalty = -3000
    infeasibilityPenalty = -10000
    priorityPenalty = -1000
    lownumberoftransplantsPenalty = -1000

    def __init__(self, chrom, pairs, patients, donors):
        self.chrom = chrom
        self.pairs = pairs
        self.patients = patients
        self.donors = donors
        self.fitness = np.Infinity
        self.chains = []
        self.cycles = []
        self.n_FeasibleNodes = 0
        self.priorityCheck = 0
                
    @staticmethod
    def determine_RandomNumberOfPairs (donors):
        randomNumber=random.randint(1,len(donors))
        return randomNumber

    @staticmethod
    def initialize (patients, donors):
        randomNumberOfPairs = Chromosome.determine_RandomNumberOfPairs (donors)        
        randomPatientsIndices = random.sample (range (len(patients)), randomNumberOfPairs)
        randomDonorsIndices = random.sample (range (len(donors)), randomNumberOfPairs)
        randomChromosome = [-1]*len(patients)
        for i in range (len (randomChromosome)) :
            for j in range (randomNumberOfPairs):
                if i == randomPatientsIndices [j]:
                    randomChromosome [i] = randomDonorsIndices [j]
                    break    
        return randomChromosome

    @staticmethod
    def detect_Pairs (chrom, patients, donors):
        pairs = []
        for i in range (len(patients)):
            if chrom [i] != -1:
                pairs.append (Pair (patients [i], donors [chrom [i]] ))
        return pairs
    
    def get_Fitness(self):
        return self.fitness

    def determine_CompatibilityFitness (self):
        compatibilityFitness = 0
        pairFitness = []

        for pair in self.pairs:
            pairFitness.append (pair.get_Fitness ())
            compatibilityFitness += self.probabilityOfRejectionPenalty * pair.patient.probabilityofRejection
        compatibilityFitness += sum (pairFitness)        

        return compatibilityFitness 

    def calculate_Fitness (self):
        totalfitness = 0
        self.priorityCheck = 0
        # cycleReward = 3000
        chainReward = 3000

        totalfitness += self.determine_CompatibilityFitness ()
        
        self.detect_CyclesAndChains()
        totalfitness += self.lownumberoftransplantsPenalty * (len (self.donors) - self.n_FeasibleNodes)
        totalfitness += (len(self.pairs) - self.n_FeasibleNodes) * self.infeasibilityPenalty
        totalfitness += self.priorityCheck * self.priorityPenalty
        # if self.cycles != []:
        #     totalfitness += cycleReward

        for i in range (len (self.chains)):
            totalfitness += chainReward
        self.fitness = copy.deepcopy (totalfitness)

    def findchain_MarketWaitlist (self):
        for pair in self.pairs:
            nodes = []
            if pair.donor.type == "market":
                if pair.patient.type == "waitlist":
                    nodes.append (pair)
                    self.chains.append (Chain (nodes))
                    self.n_FeasibleNodes += 1
                    if pair.patient.priority != 1:
                        self.priorityCheck += pair.patient.priority

    def findchain_MarketIncompatibleWaitlist (self):
        for pair in self.pairs:
            nodes = []
            if pair.donor.type == "market":
                if pair.patient.type == "incomp_patient":
                    for j in range (len(self.pairs)):
                        if pair.patient.donor.name == self.pairs[j].donor.name:
                            if self.pairs[j].patient.type == "waitlist":
                                nodes.append(pair)
                                nodes.append(self.pairs[j])
                                self.chains.append (Chain (nodes))
                                self.n_FeasibleNodes += 2
                                if self.pairs [j].patient.priority != 1:
                                    self.priorityCheck += self.pairs[j].patient.priority
    
    def findchain_Market2IncompatibleWaitlist (self):
        for pair in self.pairs:
            nodes = []
            if pair.donor.type == "market":
                if pair.patient.type == "incomp_patient":
                    for j in range (len(self.pairs)):
                        if pair.patient.donor.name == self.pairs[j].donor.name:
                            if self.pairs[j].patient.type == "incomp_patient":
                                for m in range (len(self.pairs)):
                                    if self.pairs[j].patient.donor.name == self.pairs[m].donor.name:
                                        if self.pairs[m].patient.type == "waitlist":
                                            nodes.append(pair)
                                            nodes.append(self.pairs[j])
                                            nodes.append(self.pairs[m])
                                            self.chains.append (Chain (nodes))
                                            self.n_FeasibleNodes += 3
                                            if self.pairs [m].patient.priority !=1:
                                                self.priorityCheck += self.pairs[m].patient.priority
    
    def findchain_DeceasedWaitlist (self):
        for pair in self.pairs:
            nodes = []
            if pair.donor.type == "deceased":
                if pair.patient.type == "waitlist":
                    nodes.append (pair)
                    self.chains.append (Chain (nodes))
                    self.n_FeasibleNodes += 1
                    if pair.patient.priority != 1:
                        self.priorityCheck += pair.patient.priority
    
    def findchain_DeceasedIncompatibleWaitlist (self):
        for pair in self.pairs:
            nodes = []
            if pair.donor.type == "deceased":
                if pair.patient.type == "incomp_patient":
                    for j in range (len(self.pairs)):
                        if pair.patient.donor.name == self.pairs[j].donor.name:
                            if self.pairs[j].patient.type == "waitlist":
                                nodes.append(pair)
                                nodes.append(self.pairs[j])
                                self.chains.append (Chain (nodes))
                                self.n_FeasibleNodes += 2
                                if self.pairs [j].patient.priority !=1:
                                    self.priorityCheck += self.pairs [j].patient.priority

    def findchain_Deceased2IncompatibleWaitlist (self):
        for pair in self.pairs:
            nodes = []
            if pair.donor.type == "deceased":
                if pair.patient.type == "incomp_patient":
                    for j in range (len(self.pairs)):
                        if pair.patient.donor.name == self.pairs[j].donor.name:
                            if self.pairs[j].patient.type == "incomp_patient":
                                for m in range (len(self.pairs)):
                                    if self.pairs [j].patient.donor.name == self.pairs[m].donor.name:
                                        if self.pairs [m].patient.type == "waitlist":
                                            nodes.append(pair)
                                            nodes.append(self.pairs[j])
                                            nodes.append(self.pairs[m])
                                            self.chains.append (Chain (nodes))
                                            self.n_FeasibleNodes += 3
                                            if self.pairs [m].patient.priority != 1:
                                                self.priorityCheck += self.pairs [m].patient.priority

    def findchain_IncompatibleWaitlist (self):
        for pair in self.pairs:
            nodes = []
            repetition = 0
            if (pair.donor.type == "IncompatibleRelativeDonor") or (pair.donor.type == "IncompatibleMarketDonor"):
                if pair.patient.type == "waitlist":
                    for chain in self.chains:
                        if pair in chain.nodes:
                            repetition = 1
                    if repetition == 1:
                        continue
                    nodes.append (pair)
                    self.chains.append (Chain (nodes))
                    self.n_FeasibleNodes += 1
                    if pair.patient.priority != 1:
                        self.priorityCheck += pair.patient.priority

    def findchain_2IncompatibleWaitlist (self):
        for pair in self.pairs:
            nodes = []
            repetition = 0  
            if (pair.donor.type == "IncompatibleRelativeDonor") or (pair.donor.type == "IncompatibleMarketDonor"):
                if pair.patient.type == "incomp_patient":
                    for chain in self.chains:
                        if pair in chain.nodes:
                            repetition = 1
                    if repetition ==1:
                        continue
                    for i in range (len(self.pairs)):
                        if pair.patient.donor.name == self.pairs [i].donor.name:
                            if self.pairs [i].patient.type == "waitlist":
                                nodes.append (pair)
                                nodes.append (self.pairs[i])
                                self.chains.append (Chain (nodes))
                                self.n_FeasibleNodes += 2
                                if self.pairs [i].patient.priority !=1:
                                    self.priorityCheck += self.pairs[i].patient.priority

    def findchain_3IncompatibleWaitlist (self):
        for pair in self.pairs:
            nodes = []
            if (pair.donor.type == "IncompatibleRelativeDonor") or (pair.donor.type == "IncompatibleMarketDonor"):
                if pair.patient.type == "incomp_patient":
                    for i in range (len(self.pairs)):
                        if pair.patient.donor.name == self.pairs [i].donor.name:
                            if self.pairs [i].patient.type == "incomp_patient":
                                for j in range (len(self.pairs)):
                                    if self.pairs [i].patient.donor.name == self.pairs [j].donor.name:
                                        if self.pairs [j].patient.type == "waitlist":
                                            nodes.append (pair)
                                            nodes.append (self.pairs [i])
                                            nodes.append (self.pairs [j])
                                            self.chains.append (Chain (nodes))
                                            self.n_FeasibleNodes += 3
                                            if self.pairs [j].patient.priority !=1:
                                                self.priorityCheck += self.pairs [j].patient.priority
    
    def findcycle_2Incompatible (self):        
        for pair in self.pairs:
            nodes = []
            repetition = 0
            if (pair.donor.type == "IncompatibleRelativeDonor") or (pair.donor.type == "IncompatibleMarketDonor"):
                if pair.patient.type == "incomp_patient":
                    for cycle in self.cycles:
                        if pair in cycle.nodes:
                            repetition = 1
                    if repetition ==1:
                        continue
                    for i in range (len(self.pairs)):
                        if (self.pairs [i].donor.name == pair.patient.donor.name) and (self.pairs [i].patient.name == pair.donor.patientName):
                            nodes.append (pair)
                            nodes.append (self.pairs [i])
                            self.cycles.append (Cycle (nodes))
                            self.n_FeasibleNodes += 2

    def findcycle_3Incompatible (self):
        for pair in self.pairs:
            nodes = []
            repetition = 0
            if (pair.donor.type == "IncompatibleRelativeDonor") or (pair.donor.type == "IncompatibleMarketDonor"):
                if pair.patient.type == "incomp_patient":
                    for cycle in self.cycles:
                        if pair in cycle.nodes:
                            repetition = 1
                    if repetition == 1:
                        continue
                    for i in range (len(self.pairs)):
                        if pair.patient.donor.name == self.pairs [i].donor.name :
                            if self.pairs [i].patient.type == "incomp_patient":
                                for j in range (len(self.pairs)):
                                    if self.pairs [i].patient.donor.name == self.pairs [j].donor.name:
                                        if self.pairs [j].patient.name == pair.donor.patientName:
                                            nodes.append (pair)
                                            nodes.append (self.pairs [i])
                                            nodes.append (self.pairs [j])
                                            self.cycles.append (Cycle (nodes))
                                            self.n_FeasibleNodes +=3

    def detect_CyclesAndChains (self):
        self.n_FeasibleNodes = 0
        self.cycles = []
        self.chains = []

        self.findcycle_2Incompatible ()
        self.findcycle_3Incompatible ()

        self.findchain_MarketWaitlist ()
        self.findchain_MarketIncompatibleWaitlist ()
        self.findchain_Market2IncompatibleWaitlist ()

        self.findchain_DeceasedWaitlist ()
        self.findchain_DeceasedIncompatibleWaitlist ()
        self.findchain_Deceased2IncompatibleWaitlist ()

        self.findchain_3IncompatibleWaitlist ()
        self.findchain_2IncompatibleWaitlist ()
        self.findchain_IncompatibleWaitlist () 
                               
    def mutate (self, probabilityofMutation):
        rand = random.random()
        if rand < probabilityofMutation:
            randomPoint1 = random.randint (0,len(self.chrom)-1)
            randomPoint2 = random.randint (0,len(self.chrom)-1)
            if (self.chrom [randomPoint1] == -1) and (self.chrom [randomPoint2] == -1):
                while True:
                    r = random.randint (0,len(self.donors)-1)
                    if r not in self.chrom:
                        self.chrom [randomPoint1] = r
                        break                    
            else:
                tempdonor = self.chrom [randomPoint1]
                self.chrom [randomPoint1] = self.chrom [randomPoint2]
                self.chrom [randomPoint2] = tempdonor
            self.pairs = Chromosome.detect_Pairs (self.chrom, self.patients, self.donors)

    def is_Feasible (self):        
        for i in range (len(self.pairs)):
            n=0
            for j in range (i+1,len(self.pairs)):
                if self.pairs[i].donor.type != "deceased":
                    if self.pairs[i].donor.name == self.pairs[j].donor.name:
                        return False     
                else:
                    if self.pairs[i].donor.name==self.pairs[j].donor.name:
                        n+=1
            if n>1:
                return False
        return True