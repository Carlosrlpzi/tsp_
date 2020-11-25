import copy
from abc import ABC, abstractmethod

import numpy as np

from tsp import Tour


class Algorithm(ABC):

    @abstractmethod
    def run(self, problem, *args):
        pass


class GreedyTSP(Algorithm):
    def __init__(self, **hyperparams):
        self.initial = hyperparams.get('initial')

    def run(self, tsp):
        """
        Selecciona los siguientes nodos a visitar de manera greedy
        """

        if self.initial is None:
            self.initial = np.random.choice(tsp.places)

        current = self.initial

        tour = Tour()
        tour.append(current)

        while not tour.closed:

            distances_to = {next_place: tsp.cost(current, next_place) for next_place in tsp.missing(tour.visited_places)}

            current = min(distances_to, key=distances_to.get)
            tour.append(current)

            if len(tour) == len(tsp.places):
                tour.close()

        cost = tsp.total_cost(tour)

        return {'cost': cost, 'tour': tour}

    def __str__(self):
        return f"{self.__class__} [initial: {self.initial}]"


class Ant:
    """
    Representa a un agente "hormiga" del algoritmo ACO
    """

    def __init__(self, colony, initial_state):
        self.current = initial_state
        self.tour = Tour()
        self.colony = colony

    def smell(self, other):
        return self.colony.pheromones[self.current][other]**self.colony.alpha * self.colony.eta[self.current][other]**self.colony.beta

    @property
    def not_visited(self):
        return set(self.colony.places).difference(set(self.tour))

    @property
    def tour_finished(self):
        return False if self.not_visited else True

    def move(self):
        odor = 0.0

        for next in self.not_visited:
            odor += self.smell(next)

        threshold = np.random.rand()
        for next in self.not_visited:
            prob_current_next = self.smell(next)/odor
            threshold -= prob_current_next
            if threshold <= 0:
                self.current = next
                self.tour.append(next)

    def travel(self):
        while not self.tour_finished:
            self.move()
    def __str__(self):
        return f"{self.__class__} [current: {self.current},\
         Tour: {self.current}, colony: {self.colony}]


class AntColony(Algorithm):
    """
    Implementa el algoritmo ACO básico
    """

    def __init__(self, **hyperparams):
        self.alpha = hyperparams.get('alpha', 1)
        self.beta = hyperparams.get('beta', 1)
        self.rho = hyperparams.get('rho', 0.5)
        self.Q = hyperparams.get('Q', 100)
        self.best = None
        self.steps = 0
        self.max_steps = hyperparams.get('max_steps', 100)




    def init(self):
        self.ants = [Ant(self, place) for place in self.tsp.places]
        self.initial_pheromone = 1.0/len(self.tsp.places)
        self.pheromones = np.full([len(self.tsp.places), len(
            self.tsp.places)], fill_value=self.initial_pheromone)
        self.eta = (1/self.tsp.distances)

    def reset(self):
        self.init()

    @property
    def places(self):
        return self.tsp.places

    @property
    def done(self):
        return self.steps > self.max_steps

    def update_pheromones(self):
        self.pheromones *= (1.0 - self.rho)
        self.pheromones[self.pheromones < 0.0] = self.initial_pheromone

        for ant in self.ants:
            for (current, next) in ant.tour:
                self.pheromones[current][next] += self.Q/len(ant.tour)
                self.pheromones[next][current] = self.pheromones[current][to]

        self.pheromones *= self.rho

    def update_best(self):
        for ant in self.ants:
            if len(ant.tour) < len(self.best):
                self.best = copy(ant.tour)

    def step(self):
        for ant in self.ants:
            ant.move()

        self.update_best()
        self.update_pheromones()
        self.steps += 1

    def run(self, tsp):
        self.tsp = tsp
        self.init()
        while not self.done:
            self.step()

    def __str__(self):
        return f"{self.__class__} [alpha: {self.alpha}, beta: {self.beta},\
         rho: {self.rho}, Q: {self.Q}, max_steps: {self.max_steps}]"
