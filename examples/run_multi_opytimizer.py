import numpy as np
from opytimizer import Opytimizer
from opytimizer.functions.multi import Multi
from opytimizer.optimizers.fa import FA
from opytimizer.spaces.search import SearchSpace


def sphere(x):
    # Declaring Sphere's function
    y = x ** 2

    return -np.sum(y)


def cube(x):
    # Declaring Cube's function
    y = x ** 3

    return -np.sum(y)


# Defining task's main function
z = Multi(functions=[sphere, cube], weights=[0.005, 0.5], method='weight_sum')

# Number of agents
n_agents = 20

# Number of decision variables
n_variables = 2

# Number of running iterations
n_iterations = 1000

# Lower and upper bounds (has to be the same size as n_variables)
lower_bound = [-10, -10]
upper_bound = [10, 10]

# Creating the SearchSpace class
s = SearchSpace(n_agents=n_agents, n_iterations=n_iterations,
                n_variables=n_variables, lower_bound=lower_bound,
                upper_bound=upper_bound)

# Hyperparameters for the optimizer
hyperparams = {
    'alpha': 0.5,
    'beta': 0.2,
    'gamma': 1.0
}

# Creating FA's optimizer
p = FA(hyperparams=hyperparams)

# Finally, we can create an Opytimizer class
o = Opytimizer(space=s, optimizer=p, function=z)

# Running the optimization task
history = o.start()

# Now, there is a History object holding vital historical information from the optimization task
# history.show()