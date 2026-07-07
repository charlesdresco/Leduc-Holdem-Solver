# leduc_game.py
"""
Moteur de jeu Leduc Hold'em interactif, pour jouer une main contre le solveur.
Produit des cles d'infoset identiques a celles du solveur (leduc_cfr) pour que
la strategie resolue puisse etre consultee directement.
"""

import random
from leduc_cfr import (
    card_rank, RANK_NAMES, legal_actions, round_over, showdown_u0,
    infoset_key, BET, ANTE, NUM_CARDS,
)

SUITS = ['\u2660', '\u2665']   # pique, coeur (le symbole n'affecte pas le jeu)


def card_label(idx):
    return RANK_NAMES[card_rank(idx)] + SUITS[idx % 2]


def new_hand(human_seat=None):
    if human_seat is None:
        human_seat = random.randint(0, 1)
    cards = random.sample(range(NUM_CARDS), 2)
    return {
        "cards": {0: cards[0], 1: cards[1]},
        "board": None,
        "round": 0,
        "r0hist": "",
        "r1hist": "",
        "committed": [ANTE, ANTE],
        "human_seat": human_seat,
        "done": False,
        "result_u_human": None,
        "log": [],
    }


def current_player(state):
    cur = state["r0hist"] if state["round"] == 0 else state["r1hist"]
    return len(cur) % 2


def current_infoset(state, player=None):
    if player is None:
        player = current_player(state)
    own_rank = card_rank(state["cards"][player])
    return infoset_key(own_rank, state["board"], state["round"],
                       state["r0hist"], state["r1hist"])


def legal_action_labels(state):
    cur = state["r0hist"] if state["round"] == 0 else state["r1hist"]
    facing_bet = cur.endswith('r')
    acts = legal_actions(cur)
    labels = {}
    for a in acts:
        if a == 'f':
            labels[a] = "Se coucher"
        elif a == 'c':
            labels[a] = "Suivre" if facing_bet else "Checker"
        elif a == 'r':
            labels[a] = "Relancer" if facing_bet else "Miser"
    return acts, labels


def apply_action(state, action):
    s = {
        "cards": dict(state["cards"]),
        "board": state["board"],
        "round": state["round"],
        "r0hist": state["r0hist"],
        "r1hist": state["r1hist"],
        "committed": list(state["committed"]),
        "human_seat": state["human_seat"],
        "done": False,
        "result_u_human": None,
        "log": list(state["log"]),
    }
    rnd = s["round"]
    cur = s["r0hist"] if rnd == 0 else s["r1hist"]
    actor = len(cur) % 2
    bet = BET[rnd]
    facing_bet = cur.endswith('r')

    who = "Vous" if actor == s["human_seat"] else "Le bot"
    _, labels = legal_action_labels(state)
    s["log"].append(f"{who} : {labels.get(action, action)}")

    if action == 'f':
        winner = 1 - actor
        u0 = s["committed"][1] if winner == 0 else -s["committed"][0]
        s["done"] = True
        s["result_u_human"] = u0 if s["human_seat"] == 0 else -u0
        return s

    if action == 'c':
        if facing_bet:
            s["committed"][actor] = s["committed"][1 - actor]
    elif action == 'r':
        s["committed"][actor] = max(s["committed"]) + bet

    new_cur = cur + action
    if rnd == 0:
        s["r0hist"] = new_cur
    else:
        s["r1hist"] = new_cur

    if not round_over(new_cur):
        return s

    # tour termine sans fold
    if rnd == 0:
        used = {s["cards"][0], s["cards"][1]}
        remaining = [i for i in range(NUM_CARDS) if i not in used]
        board = random.choice(remaining)
        s["board"] = board
        s["round"] = 1
        s["r1hist"] = ""
        s["log"].append(f"Carte commune revelee : {card_label(board)}")
        return s
    else:
        u0 = showdown_u0(s["cards"], s["board"], s["committed"])
        s["done"] = True
        s["result_u_human"] = u0 if s["human_seat"] == 0 else -u0
        return s


def bot_choose_action(state, strategy):
    infoset = current_infoset(state)
    probs = strategy.get(infoset)
    acts, _ = legal_action_labels(state)
    if not probs:
        return random.choice(acts)
    actions = list(probs.keys())
    weights = [probs[a] for a in actions]
    return random.choices(actions, weights=weights, k=1)[0]
