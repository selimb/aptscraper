import pytest
import random

from tarantule.core import geo


@pytest.mark.parametrize('point,expected', [
    ((0.5, 0.5), True),
    ((0.25, 0.75), True),
    ((1.5, 0.0), False),
    ((-0.5, 1.0), False),
    ((-0.5, 0.5), False),
])
def test_point_inside_square(point, expected):
    vertices = [[0, 0], [1, 0], [1, 1], [0, 1]]
    inside = geo.is_point_inside_polygon(point, vertices)
    assert inside == expected


def test_point_inside_parallelogram():
    def is_inside(point):
        x, y = point
        if y < 1 or y > 2:
            return False
        if x >= 1 and x <= 2:
            if y <= x:
                return True
        if x >= 2 and x <= 3:
            if y >= (x - 1):
                return True
        return False
    vertices = [[1, 1], [2, 1], [3, 2], [2, 2]]
    for _ in range(100):
        x = random.uniform(0, 4)
        y = random.uniform(0, 4)
        point = (x, y)
        assert geo.is_point_inside_polygon(point, vertices) == is_inside(point)
