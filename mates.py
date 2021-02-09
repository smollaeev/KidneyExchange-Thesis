import pandas as pd
import numpy as np
import random
import array
from chromosome import Chromosome
import copy

class Mates:
    def __init__(self, firstParent, secondParent, crossoverPoint, probabilityOfCrossover, patients, donors):
        self.firstParent = firstParent
        self.secondParent = secondParent
        self.crossoverPoint = crossoverPoint
        self.probabilityOfCrossover = probabilityOfCrossover
        self.patients = patients
        self.donors = donors


    def crossover(self):
        ch = []
        for p in range (len(self.firstParent.chrom)):
            if p < self.crossoverPoint:
                ch.append (self.firstParent.chrom[p])
            else:
                ch.append (self.secondParent.chrom[p])

        child = Chromosome (ch, Chromosome.detect_Pairs (ch, self.patients, self.donors), self.patients, self.donors)
        return child