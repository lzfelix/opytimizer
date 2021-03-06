import sys

import numpy as np

from opytimizer.core import function
from opytimizer.optimizers import aiwpso
from opytimizer.spaces import search
from opytimizer.utils import constants


def test_aiwpso_hyperparams():
    hyperparams = {
        'w_min': 1,
        'w_max': 3,
    }

    new_aiwpso = aiwpso.AIWPSO(hyperparams=hyperparams)

    assert new_aiwpso.w_min == 1

    assert new_aiwpso.w_max == 3


def test_aiwpso_hyperparams_setter():
    new_aiwpso = aiwpso.AIWPSO()

    try:
        new_aiwpso.w_min = 'a'
    except:
        new_aiwpso.w_min = 0.5

    try:
        new_aiwpso.w_min = -1
    except:
        new_aiwpso.w_min = 0.5

    assert new_aiwpso.w_min == 0.5

    try:
        new_aiwpso.w_max = 'b'
    except:
        new_aiwpso.w_max = 1.0

    try:
        new_aiwpso.w_max = -1
    except:
        new_aiwpso.w_max = 1.0

    try:
        new_aiwpso.w_max = 0
    except:
        new_aiwpso.w_max = 1.0

    assert new_aiwpso.w_max == 1.0


def test_aiwpso_rebuild():
    new_aiwpso = aiwpso.AIWPSO()

    assert new_aiwpso.built == True


def test_aiwpso_compute_success():
    n_agents = 2

    search_space = search.SearchSpace(n_agents=n_agents, n_iterations=10,
                                      n_variables=2, lower_bound=[0, 0],
                                      upper_bound=[10, 10])

    new_aiwpso = aiwpso.AIWPSO()

    new_fitness = np.zeros(n_agents)

    new_aiwpso._compute_success(search_space.agents, new_fitness)

    assert new_aiwpso.w != 0


def test_aiwpso_evaluate():
    def square(x):
        return np.sum(x**2)

    new_function = function.Function(pointer=square)

    search_space = search.SearchSpace(n_agents=2, n_iterations=10,
                                      n_variables=2, lower_bound=[0, 0],
                                      upper_bound=[10, 10])

    new_aiwpso = aiwpso.AIWPSO()

    local_position = np.zeros((2, 2, 1))

    new_aiwpso._evaluate(search_space, new_function, local_position)

    assert search_space.best_agent.fit < sys.float_info.max


def test_aiwpso_run():
    def square(x):
        return np.sum(x**2)

    def hook(optimizer, space, function):
        return

    new_function = function.Function(pointer=square)

    new_aiwpso = aiwpso.AIWPSO()

    search_space = search.SearchSpace(n_agents=10, n_iterations=10,
                                      n_variables=2, lower_bound=[0, 0],
                                      upper_bound=[10, 10])

    history = new_aiwpso.run(search_space, new_function, pre_evaluation_hook=hook)

    assert len(history.agents) > 0
    assert len(history.best_agent) > 0
    assert len(history.local) > 0

    best_fitness = history.best_agent[-1][1]
    assert best_fitness <= constants.TEST_EPSILON, 'The algorithm aiwpso failed to converge.'
