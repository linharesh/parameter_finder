import numpy as np
import binary_string_converter as bsc
from individual import Individual
from population import Population
from fitness_calculator import FitnessCalculator


# Classe ParameterFinder
class ParameterFinder(object):

    # Construtor da classe ParameterFinder
    # function: a função que você deseja descobrir o input
    # top: Percentual do grupo top (elite). Por exemplo: 0.2 implica em 20% de elitismo
    # bot: Percentual do grupo bottom. Por exemplo: 0.3 implica em 30% de individuos no grupo bottom
    # population_size: tamanho da população
    # dna_size: tamanho do DNA (em bits)
    # expected output: saída esperada da função
    # expected_output_type: tipo esperado da saída da função. Por exemplo: int
    # generations: Número de gerações. Por exemplo: 200
    # biased: Define se o algoritmo usado é BRKGA (True) ou RKGA(False)
    # roh: Define se o parametro roh (utilizado apenas em BRKGA)
    # verbose: Ativa ou desativa o modo verboso (imprime mais informações no console)
    def __init__(self, function, top, bot, population_size, dna_size, expected_output,
                 expected_output_type, generations, biased=False, roh=0.6, verbose=False):
        self.function = function
        self.top = top
        self.bot = bot
        self.fit_calc = FitnessCalculator(function)
        self.population = Population(population_size, dna_size)
        self.expected_output = expected_output
        self.expected_output_type = expected_output_type
        self.generations = generations
        self.biased = biased
        if self.biased:
            self.roh = roh
        else:
            self.roh = 0.5
        self.verbose = verbose


    def find_parameter(self):
        if self.expected_output_type is int:
            self.population.create_random_population()
            for generation in range(self.generations):
                fitness = self.fit_calc.calculate(self.population, self.expected_output)
                best_indv_dna = self.population.at(np.argmax(fitness)).dna
                if self.verbose:
                    print('Generation: ', str(generation), ' - ', str(bsc.nparray_binary_to_int(best_indv_dna)))
                if self.stop_condition(best_indv_dna):
                    result =  {
                        'generations': generation+1,
                        'x': int(bsc.nparray_binary_to_int(best_indv_dna)),
                        'found_x': True,
                    }
                    return result
                else:
                    self.evolve()
            return {
                'generations': generation+1,
                'x': None,
                'found_x': False,
            }
        else:
            raise Exception('Unsupported type!')

    def stop_condition(self, dna):
        return self.function(int(bsc.nparray_binary_to_int(dna))) == self.expected_output

    # No caso de RKGA, os dois indivíduos são quaisquer indivíduos da população.
    # No caso de BRKGA, o individuo indv_a é o individuo elite, e indv_b é o não elite
    def cross(self, indv_a, indv_b):
        new_dna = []
        if not self.biased:
            assert self.roh == 0.5
        for i in range(0,self.population.dna_size):
            rand_num = np.random.rand()
            if rand_num < self.roh:
                new_dna.append(indv_a.dna[i])
            else:
                new_dna.append(indv_b.dna[i])
        return Individual(new_dna)

    def reproduction(self, non_elite):
        non_elite_size = len(non_elite)
        indv_a = non_elite[np.random.randint(0,non_elite_size)]
        indv_b = non_elite[np.random.randint(0,non_elite_size)]
        return self.cross(indv_a, indv_b)

    def biased_reproduction(self, elite, non_elite):
        indv_elite = elite[np.random.randint(0,len(elite))]
        indv_non_elite = non_elite[np.random.randint(0,len(non_elite))]
        return self.cross(indv_elite, indv_non_elite)

    def evolve(self):
        elite, non_elite = self.population.split_elite(self.top)
        new_population = elite
        for i in range(0, int(self.population.size * self.bot)):
            new_population.append(Individual(np.random.uniform(0, 1, size=self.population.dna_size)))
        while len(new_population) < self.population.size:
            if self.biased:
                new_population.append(self.biased_reproduction(elite, non_elite))
            else:
                new_population.append(self.reproduction(non_elite))    
        self.population = Population(self.population.size, self.population.dna_size, new_population)
