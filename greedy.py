import numpy as np
from instances import get_instances


def greedy_knapsack(c, a, b):
    """ Heuristique gloutonne pour le problème du sac à dos multidimensionnel.

    Paramètres :
    c : Liste des gains associés aux projets.
    a : Matrice (M x N) des consommations de ressources.
    b : Liste des quantités disponibles de chaque ressource.

    Retourne :
    x : Solution binaire (0 ou 1) indiquant les projets sélectionnés.
    """

    N = len(c)  # Nombre de projets
    M = len(b)  # Nombre de ressources

    # Étape 1 : Calculer les ratios et trier les projets
    ratios = np.array(c) / (np.sum(a, axis=0) + 1e-6)  # Gain par coût total
    indices = np.argsort(-ratios)  # Trier par ratios décroissants

    # Étape 2 : Construction de la solution
    x = np.zeros(N, dtype=int)
    resource_usage = np.zeros(M)  # Suivi des ressources utilisées

    for j in indices:
        if np.all(resource_usage + a[:, j] <= b):  # Vérifier les contraintes
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
