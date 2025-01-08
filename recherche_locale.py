import numpy as np

   def is_feasible(x, a, b):
        """Vérifie si une solution est faisable."""
        return np.all(np.dot(a, x) <= b)

    def get_neighbors(x):
        """Génère les voisins en changeant un bit de la solution."""
        neighbors = []
        for i in range(len(x)):
            neighbor = x.copy()
            # Inverse le bit (ajoute ou retire un projet)
            neighbor[i] = 1 - neighbor[i]
            neighbors.append(neighbor)
        return neighbors
def local_search_knapsack(c, a, b, x_init): """ Méthode de recherche locale pour le problème du sac à dos multidimensionnel.

    Copier le code
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
        # Génère les voisins de la solution actuelle
        neighbors = get_neighbors(x_best)
        for x_neighbor in neighbors:
            if is_feasible(x_neighbor, a, b):
                neighbor_value = np.dot(c, x_neighbor)
                # Mise à jour si on trouve une meilleure solution
                if neighbor_value > best_value:
                    x_best = x_neighbor
                    best_value = neighbor_value
                    improved = True
                    break  # Sortir dès qu'une meilleure solution est trouvée
    return x_best, best_value








# Données d'exemple c = [10, 20, 15] # Gains a = np.array([[2, 3, 1], # Consommations de ressource 1 [4, 2, 3]]) # Consommations de ressource 2 b = [5, 6] # Capacités des ressources x_init = [0, 1, 0] # Solution initiale (binaire)
if name == "main":

scss
Copier le code
# Appel de la recherche locale
x_best, best_value = local_search_knapsack(c, a, b, x_init)

print("Meilleure solution trouvée :", x_best)
print("Gain total :", best_value)
