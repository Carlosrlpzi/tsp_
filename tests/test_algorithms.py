
import pytest

from tsp import Place
from tsp.algorithms import AntColony, GreedyTSP


def test_greedy(tsp_obj):

    g = GreedyTSP(initial=Place(3, 1, 1))

    solution = g.run(tsp_obj)

    assert int(solution['cost']) == 21


def test_aoc(tsp_obj):
    colony = AntColony()

    solution = colony.run(tsp_obj)

    assert solution['cost'] == 19

def test_ant(tsp_obj):
    colony = AntColony()
    place = Place(1, 1, 0)

    ant = Ant(colony, place)
    assert ant.current == place

def test_ant_smell(tsp_obj):
    pass
