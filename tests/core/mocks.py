import os
import unittest.mock

from . import samples


def network(target: str):
    """
    Network patcher decorator
    """
    return unittest.mock.patch(target, _mocked_get)

