# Metaheuristique
Dans ce projet, on s’intéresse au problème du sac à dos multidimensionnel qui consiste à maximiser le profit total en sélectionnant un sous-ensemble de projets qui respectent les contraintes de ressources disponibles. 

Vu la complexité du problème, surtout pour les instances de grande taille, on a utilisé des approches reposant sur des heuristiques, des structures de voisinage et des métaheuristiques.

Afin d'aborder ce problème, nous avons implémenté une heuristique gloutonne (greedy.py), et une heuristique de réparation (heuristique_de_reparation.py), basée dans un premier temps sur une solution initiale aléatoire et dans un second temps la relaxation surrogate. Ensuite, nous avons défini des structures de voisinage (structure_de_voisinage.py), comme la distance de Hamming et l'échange multiple (k-swap). Puis, une méthode de montée basée sur la recherche locale (recherche_locale.py) a été employée pour améliorer ces solutions initiales. Enfin, nous avons choisi l'algorithme génétique (meta_genetique.py) comme métaheuristique dans le but d'explorer efficacement des régions éloignées dans l'espace des solutions.
