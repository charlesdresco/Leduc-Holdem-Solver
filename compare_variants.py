# compare_variants.py
"""
Compare trois variantes de CFR sur le meme jeu de Leduc Hold'em :
  - CFR classique (mises a jour simultanees, moyenne uniforme)
  - CFR+ (mises a jour alternees, plancher des regrets, moyenne lineaire)
  - MCCFR external sampling (Monte Carlo)

L'axe de comparaison est le nombre de noeuds de jeu visites, qui est une mesure
honnete du cout de calcul (une iteration de MCCFR coute bien moins qu'un parcours
complet de l'arbre). On exporte les courbes dans variants_data.py.
"""

import json
from leduc_cfr import CFRPlusSolver

NODE_BUDGET = 22_000_000


def main():
    solver = CFRPlusSolver()
    print(f"{len(solver.infosets)} infosets. Budget : {NODE_BUDGET:,} noeuds par variante.")

    series = {}

    print("CFR classique...")
    h = solver.run_algo("vanilla", NODE_BUDGET, measure_current=False)
    series["CFR classique (moyenne)"] = [(n, a) for n, a, c in h]

    print("CFR+...")
    h = solver.run_algo("cfr+", NODE_BUDGET, measure_current=True)
    series["CFR+ (strategie courante)"] = [(n, c) for n, a, c in h]
    series["CFR+ (moyenne)"] = [(n, a) for n, a, c in h]

    print("MCCFR external sampling...")
    h = solver.run_algo("mccfr", NODE_BUDGET, measure_current=False)
    series["MCCFR (moyenne)"] = [(n, a) for n, a, c in h]

    # export
    data = {name: [{"nodes": n, "exploitability": e} for n, e in pts]
            for name, pts in series.items()}
    with open("variants_data.py", "w") as f:
        f.write("# Genere automatiquement par compare_variants.py\n")
        f.write("# Convergence de trois variantes de CFR, en fonction du nombre\n")
        f.write("# de noeuds de jeu visites (cout de calcul).\n")
        f.write(f"NODE_BUDGET = {NODE_BUDGET}\n")
        f.write("VARIANTS = ")
        json.dump(data, f, indent=1)
        f.write("\n")

    print("\nResume (exploitabilite au budget final) :")
    for name, pts in series.items():
        print(f"  {name:32s} -> {pts[-1][1]:.4f}")
    print("\nExporte dans variants_data.py")


if __name__ == "__main__":
    main()
