import numpy as np
from individual import Individual
from operator import attrgetter

class Population:

    # Construtor da classe Population
    # size: Número inteiro representando o tamanho da população. Exemplo: 20
    # dna_size: Número inteiro representando o tamanho do dna. Exemplo: 8 (para um dna com 8 casas 01101001)
    # individuals: Lista com indivíduos da população
    def __init__(self, size, dna_size, individuals=None):
        self.size = size
        self.dna_size = dna_size
        self.individuals = individuals

    # Cria uma nova população de forma pseudo aleatória
    def create_random_population(self):
        assert self.size is not None
        assert self.individuals is None
        assert self.size > 0
        individuals = []
        for i in range(self.size):
            individuals.append(Individual(np.random.uniform(0, 1, size=self.dna_size)))
        self.individuals = np.array(individuals)

    # Retorna o indivíduo de índice x
    def at(self, x):
        assert x is not None
        assert self.individuals is not None
        return self.individuals[x]

    # Retorna um nparray com os valores de fitness da população
    def fitness(self):
        fitness = []
        for ind in self.individuals:
            fitness.append(ind.fitness)
        return np.array(fitness)

    def split_elite(self, elitism):
        individuals = self.individuals.copy()
        individuals = sorted(individuals, key=attrgetter('fitness'), reverse=True)
        index = int(elitism * self.size)
        elite = individuals[0:index]
        non_elite = []
        for i in individuals:
            if i not in elite:
                non_elite.append(i)
        non_elite = np.array(non_elite)
        return (elite, non_elite)
