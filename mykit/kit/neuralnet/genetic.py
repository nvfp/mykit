import random as _random
import numpy as _np
from typing import (
    Callable as _Callable,
    Dict as _Dict,
    List as _List,
    Optional as _Optional,
    Tuple as _Tuple
)

from mykit.kit.neuralnet.dense import DenseNN as _DenseNN


class GeneticNN:

    def __init__(
        self,
        layer_sizes: _List[int],
        hidden_act: _Callable[[_np.ndarray, bool], _np.ndarray],
        output_act: _Callable[[_np.ndarray, bool], _np.ndarray],

        population_size: int,
        crossover_threshold: float = 0.001,
        mutation1_rate: float = 0.85,
        mutation2_rate: float = 0.99,
        mutation2_range: _Tuple[float, float] = (0.1, 2.5),
        n_new: int = 0,
        init_score: float = 0,
        
        load_wnb: _Optional[_Tuple[_List[_np.ndarray], _List[_np.ndarray]]] = None,
    ) -> None:
        """
        Genetic neural network using dense neural network.

        ---

        ## Params
        - `layer_sizes`: The size of the dense neural network for each individual.
        - `population_size`: Number of individuals per generation.
        - `crossover_threshold`: Determines how weights/biases from parent1 and parent2 are
                                 combined during crossover. If the difference between parent1
                                 and parent2 is less than this threshold, the child's value
                                 is the average; otherwise, it's randomly selected from
                                 either parent1 or parent2.
        - `mutation1_rate`: The probability of mutating a weight or bias (parent1/parent2 are close). Range: 0-1.
        - `mutation2_rate`: The probability of mutating a weight or bias (parent1/parent2 are different). Range: 0-1.
        - `mutation2_range`: The range of mutation change. For example, if set to (0.001, 0.1),
                             the weight or bias can be offset by a random value between 0.001
                             and 0.1, or between -0.001 and -0.1.
        - `n_new`: Number of new individuals (neither parent nor child) for each subsequent generation,
                   with the constraint `n_new < population_size-3`.
        - `init_score`: Initial score
        - `load_wnb`: Populate the first generation with pretrained weights and biases (use this
                      if you don't want to start the training from the beginning again).
        """

        self.layer_sizes = layer_sizes
        self.hidden_act = hidden_act
        self.output_act = output_act

        self.population_size = population_size
        self.crossover_threshold = crossover_threshold
        self.mutation1_rate = mutation1_rate
        self.mutation2_rate = mutation2_rate
        self.mutation2_range = mutation2_range
        self.n_new = n_new
        self.init_score = init_score

        self.population: _Dict[_DenseNN, float] = {}
        for _ in range(population_size):

            if load_wnb is None:
                wnb = None
            else:
                w = [w.copy() for w in load_wnb[0]]
                b = [b.copy() for b in load_wnb[1]]
                wnb = (w, b)

            nn = _DenseNN(layer_sizes, hidden_act, output_act, wnb)
            self.population[nn] = init_score


        ## runtime

        self.the_parent: _Tuple[_DenseNN, _DenseNN] = None  # to store the parent that produced the current generation (after executing `keep_elites()`)
        self.prev: _Dict[_DenseNN, float] = {}  # to store the previous generation


    def set_score(self, individual: _DenseNN, score: float, /) -> None:
        self.population[individual] = score

    def get_score(self, individual: _DenseNN, /) -> float:
        return self.population[individual]

    def get_score_min(self) -> float:
        """Return the lowest score of all individuals."""
        return min(self.population.values())

    def get_score_max(self) -> float:
        """Return the highest score of all individuals."""
        return max(self.population.values())

    def get_score_avg(self) -> float:
        """Return the average score of all individuals."""
        return sum(self.population.values()) / self.population_size

    def get_individual_by_rank(self, rank: int) -> _DenseNN:
        """Returns the individual with the given rank: 0 for the best, 1 for the second best, and so on."""
        return sorted(self.population, key=self.population.get, reverse=True)[rank]

    def get_best_individual(self) -> _DenseNN:
        """Returns the best individual (with the highest score) from the current generation."""
        return self.get_individual_by_rank(0)

    def keep_elites(self) -> None:
        """
        The idea is to continually bring out the most fit individuals from one generation to the next.
        Note: Remember to use this function after updating the scores and before executing `next_generation()`.

        ---

        What's the idea behind this function?
        =====================================

        Let's say there are only three individuals in each generation.

        - first generation -

            1. self.population = {A:0, B:0, C:0} <- each score is set to 0

            2. a new environment is set

            3. A B C undergo the scoring system and let's say the scores:
               self.population = {A:2, B:3, C:1}

            4. `keep_elites()`:

               sorted:
               {B:3, A:2, C:1}

               store the parent:
               self.the_parent = (B, A)

               store the prev:
               self.prev = self.population = {A:2, B:3, C:1}

        - 2nd generation -
            
            1. `next_generation()`:
               
               A and B are the top two, producing one child D.
               now, the current population:
               self.population = {A:0, B:0, D:0}

            2. a new environment is set

            3. A B D undergo the scoring system

            == Case I (Overall Upgrade) ==

                3. let's say the scores:
                   self.population = {A:4, B:5, D:7}

                4. `keep_elites()`:

                    picking the fitter parent:
                    comparing `self.prev = {A:2, B:3, C:1}` with `self.population = {A:4, B:5, D:7}`
                    result: self.prev = {C:1} and self.population = {A:4, B:5, D:7}

                    combine:
                    {A:4, B:5, D:7, C:1}

                    sort:
                    {D:7, B:5, A:4, C:1}

                    pick the fittest:
                    {D:7, B:5, A:4}

                    set to current population:
                    self.population = {D:7, B:5, A:4}

                    store the parent:
                    self.the_parent = (D, B)

                    stored in self.prev:
                    self.prev = self.population = {D:7, B:5, A:4}

                In other words, A and B work better in this environment.
                This is the ideal case where overall improvement occurs.

            == Case II (Overall Downgrade) ==
                
                3. let's say the scores:
                   self.population = {A:0, B:0, D:0}

                4. `keep_elites()`:

                    picking the fitter parent:
                    comparing `self.prev = {A:2, B:3, C:1}` with `self.population = {A:0, B:0, D:0}`
                    result: self.prev = {A:2, B:3, C:1} and self.population = {D:0}

                    combine:
                    {D:0, A:2, B:3, C:1}

                    sort:
                    {B:3, A:2, C:1, D:0}

                    pick the fittest:
                    {B:3, A:2, C:1}

                    set to current population:
                    self.population = {B:3, A:2, C:1}

                    ########################################################
                    let's contrast keeping the fittest from the previous generation versus not keeping them

                    if not:
                        current population:
                        self.population = {A:0, B:0, D:0}

                        potential parents: A/B or A/D or B/D
                        A/B is the same as before
                        but A/D or B/D is something different (see below for the considerations)

                    if yes:
                        current population:
                        self.population = {B:3, A:2, C:1}

                        parent: A and B
                    ########################################################
                
                    store the parent:
                    self.the_parent = (B, A)

                    stored in self.prev:
                    self.prev = self.population = {B:3, A:2, C:1}

                Note that while A B C has already experimented with 2 different environments, D has only done so once.
                In other words, the "veterans" are prioritized, meaning we stick with
                the previous generation and move to the next environment, even if A and B
                perform poorly in the current environment.

            Case III (Mix):

                3. let's say the scores:
                   self.population = {A:5, B:0, D:0}
                
                4. `keep_elites()`:

                    picking the fitter parent:
                    comparing `self.prev = {A:2, B:3, C:1}` with `self.population = {A:5, B:0, D:0}`
                    result: self.prev = {B:3, C:1} and self.population = {A:5, D:0}

                    combine:
                    {A:5, D:0, B:3, C:1}

                    sort:
                    {A:5, B:3, C:1, D:0}

                    pick the fittest:
                    {A:5, B:3, C:1}

                    set to current population:
                    self.population = {A:5, B:3, C:1}
                
                    store the parent:
                    self.the_parent = (A, B)

                    stored in self.prev:
                    self.prev = self.population = {A:5, B:3, C:1}

                In other words, stick with the previous generation and move to the next environment.
        """

        ## handle the first generation case
        if self.the_parent is None:
            parent1, parent2 = sorted(self.population, key=self.population.get, reverse=True)[:2]
            self.the_parent = (parent1, parent2)
            self.prev = self.population
        else:

            ## picking the fitter parent
            for parent in self.the_parent:
                old = self.prev[parent]
                new = self.population[parent]
                if new >= old:
                    self.prev.pop(parent)
                else:
                    self.population.pop(parent)

            ## combine
            combined = self.population
            combined.update(self.prev)

            ## sort
            sorted_ = dict(sorted(combined.items(), key=lambda item: item[1], reverse=True))

            ## pick the fittest (pick the top `self.population_size`)
            fittest = {k: sorted_[k] for k in list(sorted_)[:self.population_size]}

            ## set to current population
            self.population = fittest

            parent1, parent2 = sorted(self.population, key=self.population.get, reverse=True)[:2]
            self.the_parent = (parent1, parent2)
            self.prev = self.population

    def next_generation(self) -> None:
        """
        When executed, this function updates `self.population` by selecting the top 2 individuals
        with the highest scores from the current `self.population` and applying crossover
        and mutation to produce the new generation (the new `self.population`).

        Note: Remember to execute this after executing `keep_elites()`.

        Reminder:
        - weight and bias may have different mutation methods
        """

        ## getting the best two parents with the highest scores
        parent1, parent2 = self.the_parent

        self.population = {parent1: self.init_score, parent2: self.init_score}

        ## reproduce
        for _ in range(self.population_size-2-self.n_new):

            child = _DenseNN(self.layer_sizes, self.hidden_act, self.output_act)

            ## weights
            for l in range(len(self.layer_sizes)):  # iterate through each layer
                for c in range(self.layer_sizes[l]):  # iterate through each neuron in the current layer

                    if l != (len(self.layer_sizes)-1):
                        for s in range(self.layer_sizes[l+1]):  # iterate through each neuron in the subsequent layer
                            
                            w1 = parent1.weights[l][s, c]
                            w2 = parent2.weights[l][s, c]

                            ## crossover
                            if abs(w2-w1) < self.crossover_threshold:
                                w = (w1+w2)/2
                                ## mutation-1
                                if _random.random() < self.mutation1_rate:
                                    w = _np.random.randn()
                            else:
                                w = _random.choice([w1, w2])
                                ## mutation-2
                                if _random.random() < self.mutation2_rate:
                                    w += _random.uniform(*self.mutation2_range)*_random.choice([-1, 1])
                                    if abs(w) > 5:  # prevent explosion
                                        w = _np.random.randn()

                            child.weights[l][s, c] = w
                    
            ## biases
            for i in range(len(self.layer_sizes)-1):  # note that the input layer does not have biases
                for j in range(self.layer_sizes[i+1]):
                    
                    b1 = parent1.biases[i][j, 0]
                    b2 = parent2.biases[i][j, 0]

                    ## crossover
                    if abs(b2-b1) < self.crossover_threshold:
                        b = (b1+b2)/2
                        ## mutation-1
                        if _random.random() < self.mutation1_rate:
                            b = _np.random.randn()
                    else:
                        b = _random.choice([b1, b2])
                        ## mutation-2
                        if _random.random() < self.mutation2_rate:
                            b += _random.uniform(*self.mutation2_range)*_random.choice([-1, 1])
                            if abs(b) > 5:
                                b = _np.random.randn()

                    child.biases[i][j, 0] = b

            ## add it to the population
            self.population[child] = self.init_score

        for _ in range(self.n_new):
            self.population[_DenseNN(self.layer_sizes, self.hidden_act, self.output_act)] = self.init_score
