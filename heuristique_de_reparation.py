import numpy as np
import random
from instances import get_instances


def gen_sol_initiale(N):
    # random solution
    return [random.randint(0, 1) for _ in range(N)]


def reparation(N, M, a, b, c, x):
    """ Heuristique de réparation pour le problème du sac à dos multidimensionnel.

    Paramètres :
    N : Nombre de projets
    M : Nombre de ressources
    c : Liste des gains associés aux projets.
    a : Matrice (M x N) des consommations de ressources.
    b : Liste des quantités disponibles de chaque ressource.
    x : Solution initiale (vecteur binaire).

    Retourne :
    x : Solution binaire (0 ou 1) indiquant les projets sélectionnés.
    gain : Gain totale de la solution x réparée
    """

    # Calcul de ressouces consommées r[i] pour chaque ressource i
    r = [sum(a[i][j] * x[j] for j in range(N)) for i in range(M)]

    while any(r[i] > b[i] for i in range(M)):
        p = [(j, c[j] / sum(a[i][j] for i in range(M)))
             for j in range(N) if x[j] == 1]
        p.sort(key=lambda y: y[1])
        j_sup = p[0][0]
        x[j_sup] = 0
        for i in range(M):
            r[i] -= a[i][j_sup]

    e = [(j, c[j] / sum(a[i][j] for i in range(M)))
         for j in range(N) if x[j] == 0]
    e.sort(key=lambda y: y[1], reverse=True)
    for j, _ in e:
        if all(r[i] + a[i][j] <= b[i] for i in range(M)):
            x[j] = 1
            for i in range(M):
                r[i] += a[i][j]
    gain = sum(c[j] * x[j] for j in range(N))
    return x, gain


file_name = "instances/mknap1.txt"

instances = get_instances(file_name)
inst = instances[0]
print(inst)

N = int(inst["nb_projets"])
M = int(inst["nb_sacs"])
c = inst["gains"]
a = np.array(inst["ressources"])
b = inst["quantite_ressources"]

x = gen_sol_initiale(N)

x, gain = reparation(N, M, a, b, c, x)

print(f"Solution : {x}")
print(f"Valeur de la solution : {gain}")
print(f"Valeur optimale : {inst['opt_value']}")
