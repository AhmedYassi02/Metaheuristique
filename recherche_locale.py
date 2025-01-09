import numpy as np
from instances import get_instances
from greedy import greedy_knapsack


def is_feasible(x, a, b):
    """Vérifie si une solution est faisable."""
    return np.all(np.dot(a, x) <= b)


def get_hamming_neighbors(x):
    """Génère tous les voisins à une distance de Hamming = 1."""
    neighbors = []
    for i in range(len(x)):
        neighbor = x.copy()
        neighbor[i] = 1 - neighbor[i]  # Inverse le bit
        neighbors.append(neighbor)
    return neighbors


def local_search_knapsack(c, a, b, x_init):
    """ Méthode de recherche locale pour le problème du sac à dos multidimensionnel.

    Paramètres :
    c : Liste des gains associés aux projets.
    a : Matrice (M x N) des consommations de ressources.
    b : Liste des quantités disponibles de chaque ressource.
    x_init : Solution initiale (vecteur binaire).

    Retourne :
    x_best : Meilleure solution trouvée.
    best_value : Gain total associé à la meilleure solution.
    """

    # Initialisation
    x_best = x_init.copy()
    best_value = np.dot(c, x_best)
    improved = True

    while improved:
        improved = False
        neighbors = get_hamming_neighbors(x_best)
        for x_neighbor in neighbors:
            if is_feasible(x_neighbor, a, b):
                neighbor_value = np.dot(c, x_neighbor)

                if neighbor_value > best_value:
                    print("Nouvelle solution trouvée :", neighbor_value)
                    x_best = x_neighbor
                    best_value = neighbor_value
                    improved = True
                    break

    return x_best, best_value


file_name = "instances/mknapcb1.txt"

instances = get_instances(file_name)
inst = instances[0]

c = inst["gains"]
a = np.array(inst["ressources"])
b = inst["quantite_ressources"]


x_init, value_solution_init = greedy_knapsack(c, a, b)

x_best, best_value = local_search_knapsack(c, a, b, x_init)

print("Solution initiale :", x_init)
print("Meilleure solution trouvée :", x_best)
print("Valeur de la solution initiale :", value_solution_init)
print("Nouvelle solution :", best_value)
print("Valeur optimale :", inst['opt_value'])
