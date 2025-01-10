import numpy as np
import random
from instances import get_instances


def gen_sol_initiale(N):
    # random solution
    return [random.randint(0, 1) for _ in range(N)]


def reparation(N, M, a, b, c, x):
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


def reparation_surrogate(N, M, a, b, c, methode='simple'):

    if methode == 'simple':
        u = [1 for _ in range(M)]
    elif methode == 'inverse':
        u = [1 / b[i] for i in range(M)]
    else:
        raise ValueError("Méthode invalide")

    a_surrogate = [sum(u[i] * a[i][j] for i in range(M)) for j in range(N)]
    b_surrogate = sum(u[i] * b[i] for i in range(M))

    e = [(j, c[j] / (a_surrogate[j] + 1e-6)) for j in range(N)]
    e.sort(key=lambda y: y[1], reverse=True)

    x = [0 for i in range(N)]
    ressource = 0

    for j, _ in e:
        if ressource + a_surrogate[j] <= b_surrogate:
            x[j] = 1
            ressource += a_surrogate[j]

    r = [sum(a[i][j] * x[j] for j in range(N)) for i in range(M)]

    while any(r[i] > b[i] for i in range(M)):
        p = [(j, c[j] / a_surrogate[j]) for j in range(N) if x[j] == 1]
        p.sort(key=lambda y: y[1])
        j_sup = p[0][0]
        x[j_sup] = 0
        for i in range(M):
            r[i] -= a[i][j_sup]

    gain = sum(c[j] * x[j] for j in range(N))
    return x, gain


file_name = "instances/mknapcb3.txt"

instances = get_instances(file_name)
inst = instances[27]


N = int(inst["nb_projets"])
M = int(inst["nb_sacs"])
c = inst["gains"]
a = np.array(inst["ressources"])
b = inst["quantite_ressources"]

x = gen_sol_initiale(N)

x, gain = reparation(N, M, a, b, c, x)

print(f"Valeur optimale : {inst['opt_value']}")

# print(f"Solution : {x}")
print(f"Valeur de la solution : {gain}")

x_sur1, gain_sur1 = reparation_surrogate(N, M, a, b, c, methode='simple')

# print(f"Solution sur1 : {x_sur1}")
print(f"Valeur de la solution sur1: {gain_sur1}")

x_sur2, gain_sur2 = reparation_surrogate(N, M, a, b, c, methode='inverse')

# print(f"Solution sur2: {x_sur2}")
print(f"Valeur de la solution sur2: {gain_sur2}")
