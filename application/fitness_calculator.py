import numpy as np
import binary_string_converter

# Classe FitnessCalculator
# Esta classe é responsável por calcular o fitness de uma população
class FitnessCalculator:

    # Função que retorna a similaridade entre dois números
    @staticmethod
    def similarity(num1, num2):
        return 100 * (min(num1, num2) / max(num1, num2))

    # Construtor da classe FitnessCalculator
    def __init__(self, function):
        self.function = function

    # Calcula o fitness para uma determinada população
    # population: a população que terá o fitness calculado
    # expected_output: saída esperada
    # verbose: define se vai imprimir as operações realizadas no console
    def calculate(self, population, expected_output, verbose=False):
        fitness = []
        for indv in population.individuals:
            result = self.function(binary_string_converter.nparray_binary_to_int(indv.dna))
            indv.fitness = self.similarity(expected_output, result)
            fitness.append(indv.fitness)
            if verbose:
                print('x: ', str(binary_string_converter.nparray_binary_to_int(indv.dna)), end=' - ')
                print('y: ', str(result), end=' - ')
                print('fitness: ', str(indv.fitness))
        return np.array(fitness)
