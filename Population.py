from chromosome import Chromosome
import copy
import numpy as np
import random

class Population:
    numberOfIndividuals = 40
    crossoverPoint = 10
    probabilityOfCrossover = 1
    tournamentSize = 3
    elitismSize = 2
    probabilityOfMutation = 0.2

    def __init__(self, generation, patients, donors):
        self.generation = generation
        self.patients = patients
        self.donors = donors
        self.chromosomes = []
        self.fitness = []
        self.bestFitness = -np.Infinity
        self.bestChromosome = []
        self.averageFitness = 0
        self.elites = []     

    def initialize(self):
        pop=[]
        for _ in range(self.numberOfIndividuals):
            randomChromosome = Chromosome.initialize(self.patients, self.donors)
            pairs = Chromosome.detect_Pairs (randomChromosome, self.patients, self.donors)
            chrom = Chromosome (randomChromosome, pairs, self.patients, self.donors)
            pop.append (chrom)
            self.chromosomes = pop

    def calculate_Fitness(self):
        for chrom in self.chromosomes:
            chrom.calculate_Fitness ()
        self.__get_ChromosomesFitnesses()
        self.__find_Best()
        self.__find_Elites()

    def __get_ChromosomesFitnesses(self):
        for chrom in self.chromosomes:
            self.fitness.append (chrom.fitness)

    def __find_Best (self):
        for chrom in self.chromosomes:
            if chrom.fitness > self.bestFitness:
                self.bestFitness = chrom.fitness
                self.bestChromosome = chrom
            self.averageFitness += chrom.fitness/self.numberOfIndividuals

    def __tournamentSelect (self):
        randomIndex = random.sample (range(self.numberOfIndividuals),self.tournamentSize)
        bestFitness = -np.Infinity
        selectedChromosome = None
        for s in range (self.tournamentSize):
            if self.chromosomes [randomIndex[s]].get_Fitness() > bestFitness:
                selectedChromosome = self.chromosomes [randomIndex[s]]
                bestFitness = self.chromosomes [randomIndex[s]].get_Fitness()
        
        return selectedChromosome

    def generate_Children (self):
        childrenChromosomes = []
        while len (childrenChromosomes) < self.numberOfIndividuals-self.elitismSize:              
            child = self.__make_FeasibleChild ()
            childrenChromosomes.append (child)
        children = Population (self.generation+1, self.patients, self.donors)
        children.chromosomes = childrenChromosomes
        return children

    def __make_FeasibleChild (self):
        while True:
            firstParent = self.__tournamentSelect ()  
            secondParent = self.__tournamentSelect ()
            child = self.crossover (firstParent, secondParent)
            if child.is_Feasible ():
                break
        return child

    def crossover(self, firstParent, secondParent):
        ch = []
        for p in range (len(firstParent.chrom)):
            if p < self.crossoverPoint:
                ch.append (firstParent.chrom[p])
            else:
                ch.append (secondParent.chrom[p])

        child = Chromosome (ch, Chromosome.detect_Pairs (ch, self.patients, self.donors), self.patients, self.donors)
        return child

    def __find_Elites(self):
        ind = []
        f = copy.deepcopy (self.fitness)
        f.sort (reverse=True)
        for i in range (self.elitismSize):
            ind.append (self.fitness.index(f[i]))
        for j in range (self.elitismSize):
            self.elites.append (self.chromosomes[ind[j]])

    def mutate (self):
        while True:
            for chrom in self.chromosomes:
                chrom.mutate (self.probabilityOfMutation)
            if chrom.is_Feasible():
                break    