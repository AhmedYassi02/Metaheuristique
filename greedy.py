import numpy as np
from instances import get_instances


def greedy_knapsack(c, a, b):

    N = len(c)
    M = len(b)

    ratios = np.array(c) / (np.sum(a, axis=0) + 1e-6)
    indices = np.argsort(-ratios)

    x = np.zeros(N, dtype=int)
    resource_usage = np.zeros(M)

    for j in indices:
        if np.all(resource_usage + a[:, j] <= b):
            x[j] = 1
            resource_usage += a[:, j]
    value_solution = np.sum(c * x)

    return x, value_solution


# file_name = "instances/mknap1.txt"

# instances = get_instances(file_name)
# inst = instances[6]

# c = inst["gains"]
# a = np.array(inst["ressources"])
# b = inst["quantite_ressources"]


# x, value_solution = greedy_knapsack(c, a, b)
# print(f"Solution : {x}")
# print(f"Valeur de la solution : {value_solution}")
# print(f"Valeur optimale : {inst['opt_value']}")
