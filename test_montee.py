import time
import pandas as pd
import numpy as np
from instances import get_instances
from greedy import greedy_knapsack
from heuristique_de_reparation import gen_sol_initiale, reparation, reparation_surrogate
from recherche_locale import is_feasible, local_search, recherche_locale_combinee

def gap(solution, solution_opt):
    return ((solution_opt - solution) / solution_opt) * 100

def tester_heuristiques(instance):
    resultats = []

    for idx, inst in enumerate(instance):
        N = int(inst["nb_projets"])
        M = int(inst["nb_sacs"])
        c = inst["gains"]
        a = np.array(inst["ressources"])
        b = inst["quantite_ressources"]
        valeur_opt = inst['opt_value']
            
        # recherche locale avec solution gloutonne et Hamming 1
        start = time.time()
        x_init, _ = reparation_surrogate(N, M, a, b, c, methode='simple')
        _, solution_rep1 = local_search(N, M, c, a, b, x_init, voisinage='hamming1')
        temps_rep1 = time.time() - start
        gap_rep1 = gap(solution_rep1, valeur_opt)

        # recherche locale avec solution gloutonne et Hamming 2
        start = time.time()
        _, solution_rep2 = local_search(N, M, c, a, b, x_init, voisinage='hamming2')
        temps_rep2 = time.time() - start
        gap_rep2 = gap(solution_rep2, valeur_opt)

        # recherche locale combinée avec solution gloutonne
        start = time.time()
        _, solution_rep3 = recherche_locale_combinee(N, M, c, a, b, x_init)
        temps_rep3 = time.time() - start
        gap_rep3 = gap(solution_rep3, valeur_opt)

        # Stocker les résultats
        resultats.append({
                "Instance": idx + 1,
                "Valeur optimale": valeur_opt,
                "reparation1(solution)": solution_rep1,
                "reparation1(gap)": gap_rep1,
                "reparation1(temps)": temps_rep1,
                "reparation2(solution)": solution_rep2,
                "reparation2(gap)": gap_rep2,
                "reparation2(temps)": temps_rep2,
                "reparation3(solution)": solution_rep3,
                "reparation3(gap)": gap_rep3,
                "reparation3(temps)": temps_rep3
            })
    return pd.DataFrame(resultats)

file_name = "instances/mknap1.txt"

instance = get_instances(file_name)

df = tester_heuristiques(instance)

df_gloutonne1 = df[["Instance", "Valeur optimale", "reparation1(solution)", "reparation1(gap)", "reparation1(temps)"]]
df_gloutonne2 = df[["Instance", "Valeur optimale", "reparation2(solution)", "reparation2(gap)", "reparation2(temps)"]]
df_gloutonne3 = df[["Instance", "Valeur optimale", "reparation3(solution)", "reparation3(gap)", "reparation3(temps)"]]
df_gloutonne1.to_latex("reparation1.tex", index=False, caption="Résultats de la recherche locale sur solution d'une heuristique de reparation (Hamming 1)", label="tab:reparation1")
df_gloutonne2.to_latex("reparation2.tex", index=False, caption="Résultats de la recherche locale sur solution d'une heuristique de reparation (Hamming 2)", label="tab:reparation2")
df_gloutonne3.to_latex("reparation3.tex", index=False, caption="Résultats de la recherche locale combinée sur solution d'une heuristique de reparation", label="tab:reparation3")



