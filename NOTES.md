# Notes techniques : ce que le build a reellement appris

Trois choses qui ne viennent pas d'un tutoriel mais du debug reel, et qui font la
difference entre recopier un algorithme et le comprendre.

## 1. Mises a jour simultanees contre alternees

Ma premiere version du CFR+ convergeait en 1 sur racine de T, exactement comme le
CFR classique, alors que le CFR+ est cense etre nettement plus rapide. La cause :
je mettais a jour les deux joueurs a chaque parcours de l'arbre (simultane). Le
vrai CFR+ ne met a jour qu'un seul joueur par iteration (alterne). Apres
correction, la vitesse de convergence a change du tout au tout.

## 2. Strategie moyenne contre strategie courante

C'est le point le plus subtil. En CFR classique, seule la strategie *moyenne*
(sur toutes les iterations) converge vers l'equilibre ; la strategie de l'instant
oscille sans se stabiliser. En CFR+, la strategie *courante* converge elle aussi,
et souvent mieux que la moyenne.

J'ai observe que la moyenne du CFR+ stagnait autour de 0.05 pendant que la
courante descendait sous 0.005. La raison : la moyenne devient quasi uniforme sur
les situations rarement atteintes, car elle n'y est presque jamais mise a jour.
Or le calcul de meilleure reponse va exploiter precisement ces trous. La strategie
courante, elle, donne une reponse sensee partout grace au regret matching. C'est
pour ca que le projet exporte la strategie courante.

Correctif complementaire : pour la moyenne, sur les infosets quasi jamais
atteints, je me rabats sur la courante plutot que sur l'uniforme.

Cette difference est visible dans l'onglet de comparaison : la courbe "CFR+
strategie courante" descend bien plus bas que "CFR+ moyenne".

## 3. Comparer honnetement des algorithmes de cout different

Une iteration de MCCFR (echantillonnee) coute beaucoup moins cher qu'un parcours
complet de l'arbre. Comparer a nombre d'iterations egal serait donc trompeur. J'ai
compare en nombre de noeuds de jeu visites, ce qui reflete le vrai cout de calcul.

Resultat : sur un petit jeu comme le Leduc, les methodes a parcours complet (CFR
classique, CFR+) battent MCCFR, parce que parcourir tout l'arbre reste bon marche.
L'interet de MCCFR apparait sur les tres gros jeux, la ou parcourir l'arbre entier
est impossible et ou l'echantillonnage devient la seule option viable. Chaque
methode existe pour une raison.

Il a aussi fallu corriger l'accumulation de la moyenne en MCCFR : elle doit se
faire aux noeuds de l'adversaire echantillonne (visites a la bonne frequence), et
non a ceux du joueur qui traverse l'arbre. Sinon la moyenne est biaisee, et son
exploitabilite finit par remonter au lieu de descendre.
