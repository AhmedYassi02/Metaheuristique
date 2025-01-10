import numpy as np
import random
from heuristique_de_reparation import reparation_surrogate
from instances import get_instances

def gen_voisin_perm(N, M, a, b, c, x, max_iter=100):
    """ Génère une solution voisine, par séléction et permutation d'un projet sélectionné et 
    d'un autre non séléctionné, pour le problème du sac à dos multidimensionnel.

    Paramètres: 
    N : Nombre de projets
    M : Nombre de ressources
    c : Liste des gains associés aux projets.
    a : Matrice (M x N) des consommations de ressources.
    b : Liste des quantités disponibles de chaque ressource.
    x : Solution initiale (vecteur binaire).
    max_iter : Nombre maximal d'itération pour trouver un voisin valide.

    Retourne :
    x_vois : Solution voisine.
    """

    selec = [i for i, xi in enumerate(x) if xi == 1] # Tableau des indices des projets selectionnés dans la solution x
    non_selec = [i for i, xi in enumerate(x) if xi == 0] # Tableau des indices des projets non selectionnés dans la solution x

    for _ in range(max_iter):

        p_selec = random.choice(selec) # Choix aléatoire d'un projet selectionné
        p_non_selec = random.choice(non_selec) # Choix aléatoire d'un projet non selectionné

        x_vois = x[:]

        # permutation des deux projets

        x_vois[p_selec ] = 0 
        x_vois[p_non_selec] = 1

        # Calcul de ressouces consommées r[i] pour chaque ressource i
        r = [sum(a[i][j] * x[j] for j in range(N)) for i in range(M)]

        # Vérification des contraintes
        if all(r[i] <= b[i] for i in range(M)):
            return x_vois
    
    return x


file_name = "instances/mknap1.txt"

instances = get_instances(file_name)
inst = instances[0]


N = int(inst["nb_projets"])
M = int(inst["nb_sacs"])
c = inst["gains"]
a = np.array(inst["ressources"])
b = inst["quantite_ressources"]



x_sur2, gain_sur2 = reparation_surrogate(N, M, a, b, c, methode='inverse')

print(f"Solution sur2 : {x_sur2}")
print(f"Valeur de la solution sur2: {gain_sur2}")

x_vois = gen_voisin_perm(N, M, a, b, c, x_sur2, max_iter=100)

print(f"Solution x_vois : {x_vois}")

print(f"Valeur de la solution x_vois : {sum(c[j] * x_vois[j] for j in range(N))}")



