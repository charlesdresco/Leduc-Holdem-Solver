# leduc_cfr.py
"""
Solveur d'equilibre de Nash pour le Leduc Hold'em, via CFR+ (Counterfactual
Regret Minimization Plus), avec validation par calcul d'exploitabilite exacte
(meilleure reponse).

Leduc Hold'em est un jeu de poker de reference dans la recherche en IA :
- 6 cartes : 3 rangs (J, Q, K), 2 exemplaires de chaque.
- 2 joueurs, chacun mise 1 jeton d'ante, puis recoit 1 carte privee.
- Tour 1 : mises fixes de 2. Une carte commune est ensuite revelee.
- Tour 2 : mises fixes de 4.
- Maximum 2 relances par tour.
- A l'abattage : celui qui apparie la carte commune gagne, sinon la carte
  la plus haute l'emporte, egalite = pot partage.

Assez petit pour etre resolu exactement, assez riche pour contenir du bluff,
du semi-bluff et de la gestion de l'information cachee.
"""

import json
import math
import random

# ------------------------- Constantes du jeu -------------------------

RANKS = [0, 1, 2]              # J=0, Q=1, K=2
RANK_NAMES = {0: "J", 1: "Q", 2: "K"}
NUM_CARDS = 6                  # indices 0..5, rang = idx // 2
ANTE = 1
BET = [2, 4]                   # taille de mise par tour
MAX_RAISES = 2

FOLD, CALL, RAISE = 'f', 'c', 'r'


def card_rank(idx):
    return idx // 2


# ------------------------- Noeuds de l'arbre -------------------------

class TerminalNode:
    __slots__ = ['u0']
    def __init__(self, u0):
        self.u0 = u0            # utilite pour le joueur 0

class ChanceNode:
    __slots__ = ['children', 'prob']
    def __init__(self, children, prob):
        self.children = children   # liste de noeuds enfants
        self.prob = prob           # probabilite de chaque enfant (uniforme)

class DecisionNode:
    __slots__ = ['player', 'infoset', 'actions', 'children', 'depth']
    def __init__(self, player, infoset, actions, depth):
        self.player = player
        self.infoset = infoset
        self.actions = actions     # liste d'actions legales (chars)
        self.children = {}         # action -> noeud
        self.depth = depth


def round_over(hist):
    return hist.endswith('cc') or hist.endswith('rc')


def legal_actions(hist):
    facing_bet = hist.endswith('r')
    raises = hist.count('r')
    if facing_bet:
        acts = [FOLD, CALL]
        if raises < MAX_RAISES:
            acts.append(RAISE)
        return acts
    else:
        return [CALL, RAISE]


def infoset_key(own_rank, board, rnd, r0hist, r1hist):
    board_str = RANK_NAMES[card_rank(board)] if board is not None else '-'
    hist = r0hist + '/' + r1hist
    return f"{RANK_NAMES[own_rank]}|{board_str}|{hist}"


def showdown_u0(cards, board, committed):
    r0, r1, rb = card_rank(cards[0]), card_rank(cards[1]), card_rank(board)
    c = committed[0]
    p0pair = (r0 == rb)
    p1pair = (r1 == rb)
    if p0pair and not p1pair:
        return c
    if p1pair and not p0pair:
        return -c
    if r0 > r1:
        return c
    if r1 > r0:
        return -c
    return 0


def build_tree():
    """Construit l'arbre de jeu complet une seule fois et renvoie la racine,
    plus un dictionnaire infoset -> liste de noeuds de decision."""
    infosets = {}

    def register(node):
        infosets.setdefault(node.infoset, []).append(node)

    def build_decision(cards, board, rnd, r0hist, r1hist, committed, depth):
        cur = r0hist if rnd == 0 else r1hist
        player = len(cur) % 2
        own_rank = card_rank(cards[player])
        key = infoset_key(own_rank, board, rnd, r0hist, r1hist)
        acts = legal_actions(cur)
        node = DecisionNode(player, key, acts, depth)
        register(node)

        for a in acts:
            node.children[a] = transition(cards, board, rnd, r0hist, r1hist,
                                          committed, a, player, depth)
        return node

    def transition(cards, board, rnd, r0hist, r1hist, committed, action, actor, depth):
        cur = r0hist if rnd == 0 else r1hist
        new_committed = list(committed)
        bet = BET[rnd]
        facing_bet = cur.endswith('r')

        if action == FOLD:
            winner = 1 - actor
            u0 = new_committed[1] if winner == 0 else -new_committed[0]
            return TerminalNode(u0)

        if action == CALL:
            if facing_bet:
                new_committed[actor] = new_committed[1 - actor]
        elif action == RAISE:
            new_committed[actor] = max(new_committed) + bet

        new_cur = cur + action
        if rnd == 0:
            new_r0, new_r1 = new_cur, r1hist
        else:
            new_r0, new_r1 = r0hist, new_cur

        if not round_over(new_cur):
            return build_decision(cards, board, rnd, new_r0, new_r1, new_committed, depth + 1)

        # tour termine sans fold
        if rnd == 0:
            # noeud chance : reveler la carte commune
            used = {cards[0], cards[1]}
            remaining = [i for i in range(NUM_CARDS) if i not in used]
            children = []
            for bc in remaining:
                children.append(
                    build_decision(cards, bc, 1, new_r0, '', new_committed, depth + 1)
                )
            return ChanceNode(children, 1.0 / len(remaining))
        else:
            return TerminalNode(showdown_u0(cards, board, new_committed))

    # noeud chance racine : distribution des cartes privees (paires ordonnees)
    root_children = []
    for c0 in range(NUM_CARDS):
        for c1 in range(NUM_CARDS):
            if c0 == c1:
                continue
            root_children.append(
                build_decision((c0, c1), None, 0, '', '', [ANTE, ANTE], 0)
            )
    root = ChanceNode(root_children, 1.0 / len(root_children))
    return root, infosets


# ------------------------- CFR+ -------------------------

class CFRPlusSolver:
    def __init__(self):
        self.root, self.infosets = build_tree()
        self.regret = {}        # infoset -> {action: regret cumule}
        self.strategy_sum = {}  # infoset -> {action: proba cumulee ponderee}
        self.nodes_visited = 0  # compteur de cout de calcul
        for key, nodes in self.infosets.items():
            acts = nodes[0].actions
            self.regret[key] = {a: 0.0 for a in acts}
            self.strategy_sum[key] = {a: 0.0 for a in acts}

    def reset_tables(self):
        self.nodes_visited = 0
        for key, nodes in self.infosets.items():
            acts = nodes[0].actions
            self.regret[key] = {a: 0.0 for a in acts}
            self.strategy_sum[key] = {a: 0.0 for a in acts}

    def current_strategy(self, infoset):
        regrets = self.regret[infoset]
        pos = {a: max(r, 0.0) for a, r in regrets.items()}
        s = sum(pos.values())
        if s > 0:
            return {a: pos[a] / s for a in pos}
        n = len(regrets)
        return {a: 1.0 / n for a in regrets}

    def average_strategy(self, infoset):
        ssum = self.strategy_sum[infoset]
        s = sum(ssum.values())
        if s > 1e-12:
            return {a: ssum[a] / s for a in ssum}
        # infoset quasi jamais atteint : on se rabat sur la strategie courante
        # (mieux que l'uniforme, que la meilleure reponse exploiterait)
        return self.current_strategy(infoset)

    def _cfr(self, node, p0, p1, pc, t, update_player):
        if isinstance(node, TerminalNode):
            return node.u0
        if isinstance(node, ChanceNode):
            v = 0.0
            for child in node.children:
                v += node.prob * self._cfr(child, p0, p1, pc * node.prob, t, update_player)
            return v

        infoset = node.infoset
        player = node.player
        strat = self.current_strategy(infoset)

        au0 = {}
        node_u0 = 0.0
        for a in node.actions:
            if player == 0:
                au0[a] = self._cfr(node.children[a], p0 * strat[a], p1, pc, t, update_player)
            else:
                au0[a] = self._cfr(node.children[a], p0, p1 * strat[a], pc, t, update_player)
            node_u0 += strat[a] * au0[a]

        # CFR+ alterne : on ne met a jour que le joueur courant
        if player == update_player:
            sign = 1.0 if player == 0 else -1.0
            opp_reach = (p1 if player == 0 else p0) * pc
            own_reach = p0 if player == 0 else p1
            for a in node.actions:
                regret_inc = opp_reach * (sign * au0[a] - sign * node_u0)
                # CFR+ : regrets cumules planchés a 0
                self.regret[infoset][a] = max(0.0, self.regret[infoset][a] + regret_inc)
                # moyenne ponderee lineairement par l'iteration
                self.strategy_sum[infoset][a] += t * own_reach * strat[a]

        return node_u0

    def current_strategy_map(self):
        return {k: self.current_strategy(k) for k in self.infosets}

    def average_strategy_map(self):
        return {k: self.average_strategy(k) for k in self.infosets}

    def train(self, iterations, log_every=None, br_every=None):
        history = []
        for t in range(1, iterations + 1):
            # mises a jour alternees : un joueur par iteration
            self._cfr(self.root, 1.0, 1.0, 1.0, t, update_player=(t % 2))
            if br_every and (t % br_every == 0 or t == 1):
                expl = self.exploitability(self.current_strategy_map())
                history.append((t, expl))
                if log_every and t % log_every == 0:
                    print(f"  iter {t:5d}  exploitabilite = {expl:.6f}")
        return history

    # ------------------------- Variantes pour la comparaison -------------------------

    def _cfr_generic(self, node, p0, p1, pc, t, update_player, use_plus, avg_weight):
        """CFR parametrable. update_player=None -> mises a jour simultanees des
        deux joueurs (CFR classique). use_plus -> plancher des regrets (CFR+)."""
        self.nodes_visited += 1
        if isinstance(node, TerminalNode):
            return node.u0
        if isinstance(node, ChanceNode):
            v = 0.0
            for child in node.children:
                v += node.prob * self._cfr_generic(child, p0, p1, pc * node.prob,
                                                   t, update_player, use_plus, avg_weight)
            return v

        infoset = node.infoset
        player = node.player
        strat = self.current_strategy(infoset)

        au0 = {}
        node_u0 = 0.0
        for a in node.actions:
            if player == 0:
                au0[a] = self._cfr_generic(node.children[a], p0 * strat[a], p1, pc,
                                           t, update_player, use_plus, avg_weight)
            else:
                au0[a] = self._cfr_generic(node.children[a], p0, p1 * strat[a], pc,
                                           t, update_player, use_plus, avg_weight)
            node_u0 += strat[a] * au0[a]

        do_update = (update_player is None) or (player == update_player)
        if do_update:
            sign = 1.0 if player == 0 else -1.0
            opp_reach = (p1 if player == 0 else p0) * pc
            own_reach = p0 if player == 0 else p1
            for a in node.actions:
                inc = opp_reach * (sign * au0[a] - sign * node_u0)
                if use_plus:
                    self.regret[infoset][a] = max(0.0, self.regret[infoset][a] + inc)
                else:
                    self.regret[infoset][a] += inc
                self.strategy_sum[infoset][a] += avg_weight * own_reach * strat[a]

        return node_u0

    def _es(self, node, i, reach_i):
        """MCCFR external sampling : on echantillonne la chance et l'adversaire,
        on parcourt toutes les actions du joueur i (le traverser)."""
        self.nodes_visited += 1
        if isinstance(node, TerminalNode):
            return node.u0 if i == 0 else -node.u0
        if isinstance(node, ChanceNode):
            child = random.choice(node.children)
            return self._es(child, i, reach_i)

        infoset = node.infoset
        strat = self.current_strategy(infoset)

        if node.player == i:
            v = {}
            node_v = 0.0
            for a in node.actions:
                v[a] = self._es(node.children[a], i, reach_i * strat[a])
                node_v += strat[a] * v[a]
            for a in node.actions:
                # external sampling : pas de ponderation par le reach adverse
                self.regret[infoset][a] += (v[a] - node_v)
            return node_v
        else:
            # adversaire : ses noeuds sont visites avec une frequence
            # proportionnelle a son propre reach, donc c'est ici qu'on accumule
            # sa strategie moyenne (estimation non biaisee)
            for a in node.actions:
                self.strategy_sum[infoset][a] += strat[a]
            actions = list(strat.keys())
            weights = [strat[a] for a in actions]
            a = random.choices(actions, weights=weights, k=1)[0]
            return self._es(node.children[a], i, reach_i)

    def run_algo(self, algo, node_budget, n_measures=26, measure_current=False):
        """Entraine une variante jusqu'a un budget de noeuds visites, en mesurant
        l'exploitabilite a intervalles espaces logarithmiquement.
        Renvoie une liste de (noeuds, expl_moyenne, expl_courante_ou_None)."""
        self.reset_tables()
        start = max(1000, node_budget // 800)
        lo, hi = math.log10(start), math.log10(node_budget)
        thresholds = sorted(set(
            int(10 ** (lo + (hi - lo) * k / (n_measures - 1))) for k in range(n_measures)
        ))
        history = []
        t = 0
        idx = 0
        while self.nodes_visited < node_budget:
            t += 1
            if algo == "vanilla":
                self._cfr_generic(self.root, 1.0, 1.0, 1.0, t,
                                  update_player=None, use_plus=False, avg_weight=1.0)
            elif algo == "cfr+":
                self._cfr_generic(self.root, 1.0, 1.0, 1.0, t,
                                  update_player=(t % 2), use_plus=True, avg_weight=float(t))
            elif algo == "mccfr":
                self._es(self.root, 0, 1.0)
                self._es(self.root, 1, 1.0)
            else:
                raise ValueError(algo)
            while idx < len(thresholds) and self.nodes_visited >= thresholds[idx]:
                expl_avg = self.exploitability(self.average_strategy_map())
                expl_cur = self.exploitability(self.current_strategy_map()) if measure_current else None
                history.append((self.nodes_visited, expl_avg, expl_cur))
                idx += 1
        return history

    # ------------------------- Best response / exploitabilite -------------------------

    def exploitability(self, strategy=None):
        if strategy is None:
            strategy = self.average_strategy_map()
        br0 = self._best_response_value(strategy, 0)
        br1 = self._best_response_value(strategy, 1)
        return (br0 + br1) / 2.0

    def _best_response_value(self, avg, br_player):
        """Valeur exacte de la meilleure reponse du joueur br_player contre la
        strategie moyenne avg de l'adversaire. Calcul infoset-coherent."""
        # 1) reach de l'adversaire + chance pour chaque noeud de decision br
        opp_reach_sum = {}   # infoset br -> {action: valeur ponderee}
        infoset_depth = {}
        node_children_cache = {}

        # memo pour ev
        ev_memo = {}
        br_action = {}

        def ev(node):
            nid = id(node)
            if nid in ev_memo:
                return ev_memo[nid]
            if isinstance(node, TerminalNode):
                val = node.u0 if br_player == 0 else -node.u0
                ev_memo[nid] = val
                return val
            if isinstance(node, ChanceNode):
                val = sum(node.prob * ev(c) for c in node.children)
                ev_memo[nid] = val
                return val
            if node.player == br_player:
                a = br_action[node.infoset]        # resolu (infoset plus profond ou egal deja traite)
                val = ev(node.children[a])
                ev_memo[nid] = val
                return val
            else:
                val = sum(avg[node.infoset][a] * ev(node.children[a]) for a in node.actions)
                ev_memo[nid] = val
                return val

        # collecte des noeuds de decision br avec leur reach adverse
        br_nodes = {}   # infoset -> list of (node, opp_reach)

        def collect(node, opp_reach):
            if isinstance(node, TerminalNode):
                return
            if isinstance(node, ChanceNode):
                for c in node.children:
                    collect(c, opp_reach * node.prob)
                return
            if node.player == br_player:
                br_nodes.setdefault(node.infoset, []).append((node, opp_reach))
                infoset_depth[node.infoset] = node.depth
                for a in node.actions:
                    collect(node.children[a], opp_reach)
            else:
                for a in node.actions:
                    collect(node.children[a], opp_reach * avg[node.infoset][a])

        collect(self.root, 1.0)

        # resolution des infosets du plus profond au moins profond
        order = sorted(br_nodes.keys(), key=lambda k: infoset_depth[k], reverse=True)
        for infoset in order:
            nodes = br_nodes[infoset]
            actions = nodes[0][0].actions
            best_a, best_val = None, None
            for a in actions:
                total = 0.0
                for node, opp_reach in nodes:
                    total += opp_reach * ev(node.children[a])
                if best_val is None or total > best_val:
                    best_val, best_a = total, a
            br_action[infoset] = best_a
            # invalider le memo des noeuds de cet infoset (leur ev depend de best_a)
            for node, _ in nodes:
                ev_memo.pop(id(node), None)

        return ev(self.root)


# ------------------------- Export -------------------------

def solve_and_export(iterations=6000, br_every=120):
    print(f"Resolution du Leduc Hold'em par CFR+ ({iterations} iterations)...")
    solver = CFRPlusSolver()
    print(f"  {len(solver.infosets)} infosets dans l'arbre de jeu")
    history = solver.train(iterations, log_every=max(1, iterations // 10), br_every=br_every)

    # En CFR+, c'est la strategie COURANTE qui converge vers l'equilibre.
    strategy = solver.current_strategy_map()
    final_expl = solver.exploitability(strategy)
    print(f"Exploitabilite finale : {final_expl:.6f}")

    return solver, strategy, history, final_expl


if __name__ == "__main__":
    solver, strategy, history, final_expl = solve_and_export()

    # export strategie sous forme de module python (evite les soucis de chemin)
    convergence = [{"iteration": t, "exploitability": e} for t, e in history]
    iterations = history[-1][0] if history else 0

    with open("solved_strategy.py", "w") as f:
        f.write("# Genere automatiquement par leduc_cfr.py\n")
        f.write("# Strategie d'equilibre approche du Leduc Hold'em (CFR+)\n")
        f.write(f"ITERATIONS = {iterations}\n")
        f.write(f"FINAL_EXPLOITABILITY = {final_expl!r}\n")
        f.write(f"NUM_INFOSETS = {len(strategy)}\n")
        f.write("CONVERGENCE = ")
        json.dump(convergence, f)
        f.write("\n")
        f.write("STRATEGY = ")
        json.dump(strategy, f, indent=1)
        f.write("\n")

    print(f"{len(strategy)} infosets exportes dans solved_strategy.py")
    print(f"{len(history)} points de convergence embarques")
