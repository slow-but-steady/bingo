import numpy as np

from bingo.Base.Chromosome import Chromosome
from bingo.Base.Mutation import Mutation
from bingo.Base.Crossover import Crossover
from bingo.Base.Generator import Generator
from bingo.Util.ArgumentValidation import argument_validation


class MultipleValueChromosome(Chromosome):
    """ Multiple value individual

    The constructor for a chromosome that holds a list
    of values as opposed to a single value.

    Parameters
    ----------
    list_of_values : list of either ints, floats, or bools
        contains the chromosome's list of values

    """
    def __init__(self, list_of_values):
        super().__init__()
        self.list_of_values = list_of_values

    def __str__(self):
        return str(self.list_of_values)

    def distance(self, chromosome):
        """Computes the distance (a measure of similarity) between
        two individuals.

        Parameters
        ----------
        chromosome : MultipleValueChromosome

        Returns
        -------
        dist : float
            The distance between self and another chromosome
        """
        dist = np.sum(self.list_of_values != chromosome.list_of_values)
        return dist

class MultipleValueGenerator(Generator):
    """Generation of a population of Multi-Value Chromosomes

        Parameters
        ----------
        random_value_function : user defined function
            a function that returns a list of randomly generated values.
            This list is then passed to the ``MultipleValueChromosome``
            constructor.
        values_per_chromosome : int, default=10
            the number of values that each chromosome will hold
        """
    @argument_validation(values_per_chromosome={">=": 0})
    def __init__(self, random_value_function, values_per_chromosome):
        super().__init__()
        self._random_value_function = random_value_function
        self._values_per_chromosome = values_per_chromosome

    def __call__(self):
        """Generation of a population of size 'population_size'
        of Multi-Value Chromosomes with lists that contain
        'values_per_list' values

        Returns
        -------
        random_list :
            A list of ``MultipleValueChromosome``s
        """
        random_list = self._generate_list(self._values_per_chromosome)
        return MultipleValueChromosome(random_list)

    def _generate_list(self, number_of_values):
        return [self._random_value_function() for i in range(number_of_values)]

class SinglePointMutation(Mutation):
    """Mutation for multiple valued chromosomes

    Performs single-point mutation on the offspring of a parent chromosome.
    The mutation is performed using a user-defined mutation
    function that must return a single randomly generated value.

    Parameters
    ----------
    mutation_function : user defined function
        a function that returns a random value that will
        replace (or "mutate") a random value in a chromosome list.
    """
    def __init__(self, mutation_function):
        super().__init__()
        self._mutation_function = mutation_function

    def __call__(self, parent):
        """Performs single-point mutation using the user-defined
        mutation function passed to the constructor

        Parameters
        ----------
        parent : MultipleValueChromosome
            The parent chromosome that is copied to create
            the child that will undergo mutation

        Returns
        -------
        child : MultipleValueChromosome
                The child chromosome that has undergone mutation
        """
        child = parent.copy()
        child.fit_set = False
        mutation_point = np.random.randint(len(parent.list_of_values))
        child.list_of_values[mutation_point] = self._mutation_function()
        return child

class SinglePointCrossover(Crossover):
    """Crossover for multiple valued chromosomes

    Crossover results in two individuals with single-point crossed-over lists
    whose values are provided by the parents. Crossover point is
    a random integer produced by numpy.
    """
    def __init__(self):
        super().__init__()
        self._crossover_point = 0

    def __call__(self, parent_1, parent_2):
        """Performs single-point crossover of two parent chromosomes

        Parameters
        ----------
        parent_1 : MultipleValueChromosome
            the first parent to be used for crossover
        parent_2 : MultipleValueChromosome
            the second parent to be used for crossover

        Returns
        -------
        child_1, child_2 : tuple of MultiValueChromosome
            a tuple of the 2 children produced by crossover
        """
        child_1 = parent_1.copy()
        child_2 = parent_2.copy()
        child_1.fit_set = False
        child_2.fit_set = False
        self._crossover_point = np.random.randint(len(parent_1.list_of_values))
        child_1.list_of_values = parent_1.list_of_values[:self._crossover_point] + parent_2.list_of_values[self._crossover_point:]
        child_2.list_of_values = parent_2.list_of_values[:self._crossover_point] + parent_1.list_of_values[self._crossover_point:]
        if parent_1.genetic_age > parent_2.genetic_age:
            age = parent_1.genetic_age
        else:
            age = parent_2.genetic_age
        child_1.genetic_age = age
        child_2.genetic_age = age
        return child_1, child_2
