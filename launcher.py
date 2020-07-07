from parameter_finder import ParameterFinder
import math

if __name__ == '__main__':

    param_finder = ParameterFinder(function=math.factorial, 
                                   top=0.2,
                                   bot=0.4,
                                   population_size=40,
                                   dna_size=8,
                                   expected_output=5040,
                                   expected_output_type=int,
                                   generations=500,
                                   biased=True,
                                   verbose=True)

    print(param_finder.find_parameter())
