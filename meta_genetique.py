import random
from instances import get_instances
import numpy as np
from heuristique_de_reparation import reparation, gen_sol_initiale
from structure_de_voisinage import gen_voisin_perm


def gen_random_sols(N, M, a, b, c, n_sols):
    first_rd_sol = gen_sol_initiale(N)
    feasible_sol, _ = reparation(N, M, a, b, c, first_rd_sol)

    # On génère n_sols solutions aléatoires on explorant les voisinages
    sols = [feasible_sol]
    for _ in range(n_sols-1):
        x = feasible_sol.copy()
        for _ in range(10):
            x = gen_voisin_perm(N, M, a, b, c, x)
        sols.append(x)

    return sols


def is_feasible(x, a, b):
    """Vérifie si une solution est faisable."""
    return np.all(np.dot(a, x) <= b)


def mutate_solution(N, M, a, b, c, x):
    x_mut = x.copy()
    i = random.randint(0, len(x)-1)
    x_mut[i] = 1 - x_mut[i]
    x_mut = reparation(N, M, a, b, c, x_mut)[0]
    return x_mut


def cross_over(x1, x2):
    x_cross = x1.copy()
    i = random.randint(0, len(x1)-1)
    x_cross[i:] = x2[i:]
    x_cross = reparation(N, M, a, b, c, x_cross)[0]
    return x_cross


def genetic_algo(N, M, c, a, b, max_iter=100, pop_size=100):
    """ Méthode de recherche locale pour le problème du sac à dos multidimensionnel.

    Paramètres :
    c : Liste des gains associés aux projets.
    a : Matrice (M x N) des consommations de ressources.
    b : Liste des quantités disponibles de chaque ressource.
    max_iter : Nombre maximal d'itérations.
    pop_size : Taille de la population.

    Retourne :
    x_best : Meilleure solution trouvée.
    best_value : Gain total associé à la meilleure solution.
    """

    N = len(c)
    M = len(b)
    population = gen_random_sols(N, M, a, b, c, pop_size)
    best_value = 0
    x_best = population[0]

    for _ in range(max_iter):
        values = [sum(c[j] * x[j] for j in range(N)) for x in population]

        best_idx = values.index(max(values))
        second_best_idx = values.index(
            max([values[i] for i in range(pop_size) if i != best_idx]))

        if values[best_idx] > best_value:
            x_best = population[best_idx]
            best_value = values[best_idx]

        x1 = population[best_idx]
        x2 = population[second_best_idx]
        x_cross = cross_over(x1, x2)

        x_mut = mutate_solution(N, M, a, b, c, x_cross)

        worst_idx = values.index(min(values))
        population[worst_idx] = x_mut
        print(
            f"Nouvelle solution trouvée :{best_value} : {is_feasible(x_best, a, b)}")

    return x_best, best_value


file_name = "instances/mknap1.txt"

instances = get_instances(file_name)
inst = instances[6]

c = inst["gains"]
a = np.array(inst["ressources"])
b = inst["quantite_ressources"]
N = len(c)
M = len(b)

print("BEST VALUE :", inst["opt_value"])

x_best, best_value = genetic_algo(N, M, c, a, b, max_iter=100, pop_size=100)
print(f"gap :  {( inst['opt_value']-best_value)/inst['opt_value']*100}%")

print(is_feasible(x_best, a, b))
