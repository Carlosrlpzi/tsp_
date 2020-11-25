import pytest

from tsp import Place, Tour


def test_tour_cost(tsp_obj, tour_obj):
    assert [tsp_obj.cost(current, next)
            for current, next in tour_obj] == [3, 6, 5, 8, 7]
    assert tsp_obj.total_cost(tour_obj) == 29


def test_tsp_creation(tsp_obj):
    assert Place(0, 0, 0) == tsp_obj.places[0] and \
        Place(1, 1, 0) == tsp_obj.places[1] and \
        Place(2, 0, 1) == tsp_obj.places[2] and \
        Place(3, 1, 1) == tsp_obj.places[3] and \
        Place(4, 2, 3) == tsp_obj.places[4]

def test_missing_places(tsp_obj):
    t1 = Tour()
    t2 = Tour()
    t1.append(places['A'])
    t1.append(places['B'])
    t1.append(places['C'])

    t2.append(places['D'])

    assert t1.missing(places.values()) == set(t2._path)
