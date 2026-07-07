# Leduc Hold'em Solver

Un solveur d'equilibre de Nash pour le **Leduc Hold'em**, ecrit de zero, avec
une application interactive pour explorer la strategie et jouer contre elle.

La strategie n'est pas ecrite a la main. Elle est **calculee** par l'algorithme
**CFR+** (Counterfactual Regret Minimization Plus), puis **validee
mathematiquement** par le calcul exact de son exploitabilite.

## Pourquoi le Leduc Hold'em

Le Leduc Hold'em est un jeu de poker simplifie qui sert de banc d'essai standard
dans la recherche en IA (il apparait dans les travaux fondateurs sur le poker,
comme ceux de l'universite d'Alberta). Il est assez petit pour etre resolu
exactement, mais assez riche pour contenir de vrais concepts de poker : bluff,
semi-bluff, ralentissement du jeu, gestion de l'information cachee.

Regles :
- 6 cartes : trois rangs (Valet, Dame, Roi), deux exemplaires de chacun.
- Deux joueurs misent 1 jeton d'ante, puis recoivent une carte privee.
- Tour 1 : mises fixes de 2. Une carte commune est ensuite revelee.
- Tour 2 : mises fixes de 4. Deux relances maximum par tour.
- A l'abattage : apparier la carte commune gagne, sinon la carte la plus haute
  l'emporte, egalite = pot partage.

## Ce que fait le projet

1. **Construit l'arbre de jeu complet** une seule fois : 288 ensembles
   d'information, ce qui correspond au chiffre connu pour le Leduc.
2. **Resout le jeu par CFR+** avec mises a jour alternees et moyenne ponderee.
3. **Mesure l'exploitabilite exacte** via un calcul de meilleure reponse
   coherent par ensemble d'information (l'adversaire ne voit pas les cartes
   privees). C'est la validation rigoureuse : a l'equilibre de Nash,
   l'exploitabilite vaut zero.
4. **Expose le tout dans une application** avec trois onglets : vue d'ensemble
   et courbe de convergence, explorateur de strategie, et un mode pour jouer une
   main contre le solveur.

## Resultat

- 288 ensembles d'information.
- Apres 6000 iterations de CFR+, exploitabilite d'environ **0.0043**.
- La strategie retrouve seule des idees de poker : miser fort ses meilleures
  mains, bluffer parfois ses pires mains face a une mise, et ralentir le jeu
  (checker une main tres forte pour relancer ensuite).

## Comparaison de trois algorithmes

Le projet ne se contente pas d'un seul algorithme. Il compare, sur le meme jeu,
trois methodes de la famille CFR : le CFR classique, le CFR+, et le MCCFR
(Monte Carlo CFR, echantillonne). La comparaison se fait en nombre de noeuds de
jeu visites, ce qui reflete le vrai cout de calcul. Elle met aussi en evidence
une subtilite : en CFR+, la strategie courante converge mieux que la moyenne.
Voir `NOTES.md` et l'onglet de comparaison de l'application.

## Fichiers

- `leduc_cfr.py` : moteur, construction de l'arbre, les trois variantes de CFR,
  meilleure reponse et exploitabilite. Lancer `python3 leduc_cfr.py` recalcule
  tout et regenere la strategie.
- `compare_variants.py` : compare les trois algorithmes et exporte les courbes.
- `leduc_game.py` : moteur de jeu interactif pour jouer une main.
- `solved_strategy.py` : strategie resolue et courbe de convergence.
- `variants_data.py` : courbes de comparaison des algorithmes.
- `streamlit_app.py` : l'application (5 onglets).
- `NOTES.md` : les enseignements techniques du build.

## Lancer en local

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Recalculer la strategie

```bash
python3 leduc_cfr.py
```

## Relancer la comparaison des algorithmes

```bash
python3 compare_variants.py
```

## Note d'honnetete

C'est un solveur pour le Leduc Hold'em, pas pour le No-Limit Texas Hold'em
complet. Le No-Limit reel a un espace de jeu des milliards de fois plus grand et
demande des techniques supplementaires (abstraction, echantillonnage). L'interet
de ce projet est que, sur un jeu ou la verite est calculable, tout est fait
proprement et verifiable : la strategie est reellement calculee et son ecart a
l'optimum est mesure exactement.
