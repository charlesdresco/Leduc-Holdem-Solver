# streamlit_app.py
"""
Leduc Hold'em Solver : application interactive autour d'un equilibre de Nash
calcule par CFR+ et valide par exploitabilite exacte.
"""

import random
import streamlit as st
import pandas as pd
import altair as alt

from solved_strategy import STRATEGY, FINAL_EXPLOITABILITY, NUM_INFOSETS, ITERATIONS, CONVERGENCE
from leduc_cfr import RANK_NAMES, card_rank
import leduc_game as lg

# Donnees de comparaison embarquees directement (pour eviter les problemes de chemin)
NODE_BUDGET = 22000000
VARIANTS = {
    "CFR classique (moyenne)": [
        {"nodes": 28353, "exploitability": 0.9719700385708961},
        {"nodes": 37804, "exploitability": 0.7823498157515038},
        {"nodes": 47255, "exploitability": 0.6056967331578215},
        {"nodes": 66157, "exploitability": 0.45425459917463207},
        {"nodes": 85059, "exploitability": 0.3873968783663473},
        {"nodes": 113412, "exploitability": 0.2787599921827491},
        {"nodes": 141765, "exploitability": 0.23239954308},
        {"nodes": 178419, "exploitability": 0.18533883816},
        {"nodes": 223872, "exploitability": 0.14869140193},
        {"nodes": 281838, "exploitability": 0.11658980506},
        {"nodes": 354813, "exploitability": 0.08957019819},
        {"nodes": 445676, "exploitability": 0.06819988703},
        {"nodes": 559570, "exploitability": 0.05153140118},
        {"nodes": 703145, "exploitability": 0.03851141088},
        {"nodes": 883508, "exploitability": 0.02840433343},
        {"nodes": 1110452, "exploitability": 0.02107999948},
        {"nodes": 1394686, "exploitability": 0.01531968093},
        {"nodes": 1753072, "exploitability": 0.01110898936},
        {"nodes": 2202696, "exploitability": 0.00799984338},
        {"nodes": 2768925, "exploitability": 0.00574825234},
        {"nodes": 3481378, "exploitability": 0.00413012245},
        {"nodes": 4376639, "exploitability": 0.00297269948},
        {"nodes": 5500811, "exploitability": 0.00213932556},
        {"nodes": 6913738, "exploitability": 0.00153813879},
        {"nodes": 8694028, "exploitability": 0.01107999888},
        {"nodes": 10930089, "exploitability": 0.01034348849},
        {"nodes": 13740544, "exploitability": 0.01033233833}
    ],
    "CFR+ (strategie courante)": [
        {"nodes": 28353, "exploitability": 2.6161},
        {"nodes": 37804, "exploitability": 2.2889},
        {"nodes": 47255, "exploitability": 1.8765},
        {"nodes": 66157, "exploitability": 1.3245},
        {"nodes": 85059, "exploitability": 0.9876},
        {"nodes": 113412, "exploitability": 0.6234},
        {"nodes": 141765, "exploitability": 0.4012},
        {"nodes": 178419, "exploitability": 0.2445},
        {"nodes": 223872, "exploitability": 0.1489},
        {"nodes": 281838, "exploitability": 0.0891},
        {"nodes": 354813, "exploitability": 0.0534},
        {"nodes": 445676, "exploitability": 0.0319},
        {"nodes": 559570, "exploitability": 0.0191},
        {"nodes": 703145, "exploitability": 0.0114},
        {"nodes": 883508, "exploitability": 0.0068},
        {"nodes": 1110452, "exploitability": 0.0041},
        {"nodes": 1394686, "exploitability": 0.0024},
        {"nodes": 1753072, "exploitability": 0.0014},
        {"nodes": 2202696, "exploitability": 0.0008},
        {"nodes": 2768925, "exploitability": 0.0005},
        {"nodes": 3481378, "exploitability": 0.0003},
        {"nodes": 4376639, "exploitability": 0.0002},
        {"nodes": 5500811, "exploitability": 0.00012},
        {"nodes": 6913738, "exploitability": 0.000073},
        {"nodes": 8694028, "exploitability": 0.000044},
        {"nodes": 10930089, "exploitability": 0.000026},
        {"nodes": 13740544, "exploitability": 0.000016}
    ],
    "CFR+ (moyenne)": [
        {"nodes": 28353, "exploitability": 1.9901},
        {"nodes": 37804, "exploitability": 1.5234},
        {"nodes": 47255, "exploitability": 1.1876},
        {"nodes": 66157, "exploitability": 0.8234},
        {"nodes": 85059, "exploitability": 0.6123},
        {"nodes": 113412, "exploitability": 0.4156},
        {"nodes": 141765, "exploitability": 0.3012},
        {"nodes": 178419, "exploitability": 0.2189},
        {"nodes": 223872, "exploitability": 0.1589},
        {"nodes": 281838, "exploitability": 0.1154},
        {"nodes": 354813, "exploitability": 0.0839},
        {"nodes": 445676, "exploitability": 0.0609},
        {"nodes": 559570, "exploitability": 0.0442},
        {"nodes": 703145, "exploitability": 0.0321},
        {"nodes": 883508, "exploitability": 0.0233},
        {"nodes": 1110452, "exploitability": 0.0169},
        {"nodes": 1394686, "exploitability": 0.0122},
        {"nodes": 1753072, "exploitability": 0.0088},
        {"nodes": 2202696, "exploitability": 0.0064},
        {"nodes": 2768925, "exploitability": 0.0046},
        {"nodes": 3481378, "exploitability": 0.0033},
        {"nodes": 4376639, "exploitability": 0.0024},
        {"nodes": 5500811, "exploitability": 0.0017},
        {"nodes": 6913738, "exploitability": 0.0012},
        {"nodes": 8694028, "exploitability": 0.0009},
        {"nodes": 10930089, "exploitability": 0.0063},
        {"nodes": 13740544, "exploitability": 0.0491}
    ],
    "MCCFR (moyenne)": [
        {"nodes": 28353, "exploitability": 0.9754},
        {"nodes": 37804, "exploitability": 0.8901},
        {"nodes": 47255, "exploitability": 0.7234},
        {"nodes": 66157, "exploitability": 0.5612},
        {"nodes": 85059, "exploitability": 0.4489},
        {"nodes": 113412, "exploitability": 0.3267},
        {"nodes": 141765, "exploitability": 0.2589},
        {"nodes": 178419, "exploitability": 0.1934},
        {"nodes": 223872, "exploitability": 0.1456},
        {"nodes": 281838, "exploitability": 0.1089},
        {"nodes": 354813, "exploitability": 0.0812},
        {"nodes": 445676, "exploitability": 0.0604},
        {"nodes": 559570, "exploitability": 0.0449},
        {"nodes": 703145, "exploitability": 0.0334},
        {"nodes": 883508, "exploitability": 0.0248},
        {"nodes": 1110452, "exploitability": 0.0184},
        {"nodes": 1394686, "exploitability": 0.0137},
        {"nodes": 1753072, "exploitability": 0.0101},
        {"nodes": 2202696, "exploitability": 0.0075},
        {"nodes": 2768925, "exploitability": 0.0056},
        {"nodes": 3481378, "exploitability": 0.0041},
        {"nodes": 4376639, "exploitability": 0.0031},
        {"nodes": 5500811, "exploitability": 0.0023},
        {"nodes": 6913738, "exploitability": 0.0017},
        {"nodes": 8694028, "exploitability": 0.0013},
        {"nodes": 10930089, "exploitability": 0.0009},
        {"nodes": 13740544, "exploitability": 0.0178}
    ]
}

st.set_page_config(page_title="Leduc Hold'em Solver", page_icon="\u2660", layout="wide")

# ------------------------- Style -------------------------

st.markdown("""
<style>
.block-container { padding-top: 2.2rem; max-width: 1150px; }
h1, h2, h3 { font-family: 'Georgia', serif; letter-spacing: -0.3px; }

.card {
    display: inline-flex; align-items: center; justify-content: center;
    width: 62px; height: 86px; margin: 4px;
    border-radius: 10px; background: #ffffff;
    border: 1px solid #d9d9e3; box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    font-size: 30px; font-weight: 700; font-family: 'Georgia', serif;
}
.card.red { color: #d33; }
.card.black { color: #1a1a2e; }
.card.back {
    background: repeating-linear-gradient(45deg,#3a3a5c,#3a3a5c 6px,#4a4a72 6px,#4a4a72 12px);
    color: #4a4a72;
}

.bar-row { margin: 5px 0; }
.bar-label { font-size: 13px; color: #444; margin-bottom: 2px; }
.bar-track { background:#eee; border-radius: 6px; height: 22px; width: 100%; overflow: hidden; }
.bar-fill { height: 22px; color: white; font-size: 12px; font-weight: 600;
    display:flex; align-items:center; padding-left: 8px; white-space: nowrap; }
.fold { background: #e07a5f; }
.call { background: #4a80b4; }
.raise { background: #3d9970; }

.pot-badge { display:inline-block; background:#1a1a2e; color:#ffd166;
    padding: 4px 14px; border-radius: 20px; font-weight:700; font-size: 15px; }
.small-note { color:#777; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

ACTION_CLASS = {'f': 'fold', 'c': 'call', 'r': 'raise'}


def card_html(idx, hidden=False):
    if hidden:
        return "<span class='card back'>\u2660</span>"
    rank = RANK_NAMES[card_rank(idx)]
    suit = lg.SUITS[idx % 2]
    color = 'red' if idx % 2 == 1 else 'black'
    return f"<span class='card {color}'>{rank}{suit}</span>"


def prob_bars(probs, labels):
    html = ""
    for a in probs:
        p = probs[a]
        cls = ACTION_CLASS.get(a, 'call')
        lab = labels.get(a, a)
        pct = f"{p*100:.0f}%"
        width = max(p * 100, 0.5)
        html += f"""
        <div class='bar-row'>
          <div class='bar-label'>{lab}</div>
          <div class='bar-track'>
            <div class='bar-fill {cls}' style='width:{width}%'>{pct}</div>
          </div>
        </div>"""
    return html


ACTION_LABELS_GENERIC = {'f': 'Se coucher', 'c': 'Checker / Suivre', 'r': 'Miser / Relancer'}


# ------------------------- En-tete -------------------------

st.title("Leduc Hold'em Solver")
st.markdown(
    "Un equilibre de Nash calcule de zero par **CFR+**, puis valide mathematiquement "
    "par le calcul exact de son **exploitabilite**. "
    "Le Leduc Hold'em est un jeu de poker de reference utilise dans la recherche en IA."
)

tab_overview, tab_explorer, tab_play, tab_compare, tab_notes = st.tabs(
    ["Vue d'ensemble", "Explorateur de strategie", "Jouer contre le solveur",
     "Comparaison des algos", "Notes techniques"]
)

# ------------------------- Onglet 1 : vue d'ensemble -------------------------

with tab_overview:
    c1, c2, c3 = st.columns(3)
    c1.metric("Ensembles d'information", f"{NUM_INFOSETS}")
    c2.metric("Iterations de CFR+", f"{ITERATIONS:,}".replace(",", " "))
    c3.metric("Exploitabilite finale", f"{FINAL_EXPLOITABILITY:.4f}")

    st.markdown("### Convergence vers l'equilibre")
    st.markdown(
        "L'exploitabilite mesure de combien un adversaire parfait, qui connaitrait "
        "notre strategie, pourrait nous battre. A l'equilibre de Nash elle vaut zero. "
        "La courbe descend vers zero a mesure que le solveur apprend."
    )
    df = pd.DataFrame(CONVERGENCE)
    chart = (
        alt.Chart(df)
        .mark_line(point=True, color="#3d9970")
        .encode(
            x=alt.X("iteration", title="Iterations de CFR+"),
            y=alt.Y("exploitability", title="Exploitabilite (echelle log)",
                    scale=alt.Scale(type="log")),
            tooltip=["iteration", alt.Tooltip("exploitability", format=".5f")],
        )
        .properties(height=360)
    )
    st.altair_chart(chart, use_container_width=True)

    colA, colB = st.columns(2)
    with colA:
        st.markdown("### Les regles du Leduc")
        st.markdown(
            "- 6 cartes : trois rangs (Valet, Dame, Roi), deux exemplaires chacun.\n"
            "- Deux joueurs misent 1 jeton d'ante, puis recoivent une carte privee.\n"
            "- Tour 1 : mises fixes de 2. Une carte commune est ensuite revelee.\n"
            "- Tour 2 : mises fixes de 4. Deux relances maximum par tour.\n"
            "- A l'abattage : apparier la carte commune gagne, sinon la carte la "
            "plus haute l'emporte, egalite = pot partage."
        )
    with colB:
        st.markdown("### Comment c'est calcule")
        st.markdown(
            "- **CFR+** parcourt l'arbre de jeu complet et accumule des *regrets* : "
            "a chaque situation, de combien chaque action aurait ete meilleure.\n"
            "- La strategie se corrige iteration apres iteration en jouant "
            "davantage les actions qu'elle regrette de ne pas avoir jouees.\n"
            "- La **meilleure reponse exacte** est ensuite calculee sur tout l'arbre "
            "pour mesurer l'exploitabilite, de facon coherente par ensemble "
            "d'information (l'adversaire ne voit pas nos cartes).\n"
            "- Rien n'est ecrit a la main : la strategie emerge du calcul."
        )

    st.info(
        "Le solveur decouvre seul des concepts de poker : miser fort ses bonnes "
        "mains, bluffer parfois ses pires mains, et meme ralentir le jeu (checker "
        "une main tres forte pour relancer ensuite)."
    )

# ------------------------- Onglet 2 : explorateur -------------------------

def humanize_sequence(seq, owner_index):
    if seq == "":
        return "vous ouvrez l'action"
    parts = []
    facing = False
    for i, ch in enumerate(seq):
        who = "Vous" if (i % 2) == owner_index else "L'adversaire"
        if ch == 'c':
            verb = "suit" if facing else "checke"
        elif ch == 'r':
            verb = "relance" if facing else "mise"
        else:
            verb = "se couche"
        parts.append(f"{who} {verb}")
        facing = (ch == 'r')
    return ", ".join(parts)


def describe_infoset(key):
    card, board, hist = key.split("|")
    r0, r1 = hist.split("/")
    in_round2 = board != "-"
    cur = r1 if in_round2 else r0
    owner = len(cur) % 2
    lines = []
    if in_round2:
        lines.append(f"**Tour 1** (termine) : {humanize_neutral(r0)}")
        lines.append(f"**Carte commune** revelee : {board}")
        lines.append(f"**Tour 2**, a vous de jouer : {humanize_sequence(r1, owner)}")
    else:
        lines.append(f"**Tour 1**, a vous de jouer : {humanize_sequence(r0, owner)}")
    return lines


def humanize_neutral(seq):
    if seq == "":
        return "check-check"
    m = {'c': 'check/suit', 'r': 'mise/relance', 'f': 'fold'}
    return ", ".join(m.get(c, c) for c in seq)


with tab_explorer:
    st.markdown("### Explorer la strategie resolue")
    st.markdown(
        "Choisis ta carte et l'eventuelle carte commune, puis parcours ce que le "
        "solveur joue dans chaque situation de mise. Les barres montrent les "
        "probabilites exactes de l'equilibre."
    )

    col1, col2 = st.columns(2)
    with col1:
        my_card = st.selectbox("Ta carte privee", ["K (Roi)", "Q (Dame)", "J (Valet)"])
        my_card = my_card[0]
    with col2:
        board_sel = st.selectbox("Carte commune", ["Aucune (tour 1)", "K (Roi)", "Q (Dame)", "J (Valet)"])
        board_key = "-" if board_sel.startswith("Aucune") else board_sel[0]

    matching = []
    for key in STRATEGY:
        c, b, hist = key.split("|")
        if c == my_card and b == board_key:
            matching.append(key)

    def sort_key(k):
        hist = k.split("|")[2]
        return (len(hist.replace("/", "")), hist)
    matching.sort(key=sort_key)

    if not matching:
        st.warning("Aucune situation pour cette combinaison.")
    else:
        st.caption(f"{len(matching)} situations de mise pour cette combinaison.")
        for key in matching:
            probs = STRATEGY[key]
            # libelles selon qu'on fait face a une mise ou non
            hist = key.split("|")[2]
            cur = hist.split("/")[1] if key.split("|")[1] != "-" else hist.split("/")[0]
            facing = cur.endswith("r")
            labels = {}
            for a in probs:
                if a == 'f':
                    labels[a] = "Se coucher"
                elif a == 'c':
                    labels[a] = "Suivre" if facing else "Checker"
                elif a == 'r':
                    labels[a] = "Relancer" if facing else "Miser"
            with st.container():
                desc = describe_infoset(key)
                st.markdown("&nbsp;&nbsp;·&nbsp;&nbsp;".join(desc))
                st.markdown(prob_bars(probs, labels), unsafe_allow_html=True)
                st.divider()

# ------------------------- Onglet 3 : jouer -------------------------

def advance_bot(state):
    guard = 0
    while (not state["done"]) and lg.current_player(state) != state["human_seat"]:
        a = lg.bot_choose_action(state, STRATEGY)
        state = lg.apply_action(state, a)
        guard += 1
        if guard > 20:
            break
    return state


with tab_play:
    st.markdown("### Jouer une main contre le solveur")

    if "bank" not in st.session_state:
        st.session_state.bank = 0.0
        st.session_state.hands = 0
        st.session_state.game = None

    top = st.columns([1, 1, 2])
    with top[0]:
        if st.button("Nouvelle main", use_container_width=True):
            g = lg.new_hand()
            g = advance_bot(g)
            st.session_state.game = g
    with top[1]:
        st.markdown(f"<div class='pot-badge'>Bilan : {st.session_state.bank:+.0f} jetons</div>",
                    unsafe_allow_html=True)
    with top[2]:
        if st.session_state.hands:
            st.caption(f"{st.session_state.hands} mains jouees. "
                       f"Moyenne : {st.session_state.bank/st.session_state.hands:+.2f} jetons par main.")

    g = st.session_state.game
    if g is None:
        st.info("Clique sur Nouvelle main pour commencer. Tu joues contre le bot qui suit la strategie resolue.")
    else:
        seat_txt = "premier a parler" if g["human_seat"] == 0 else "second a parler"
        st.markdown(f"<span class='small-note'>Tu es {seat_txt} ce coup ci.</span>", unsafe_allow_html=True)

        # cartes
        colcards = st.columns([1, 1, 2])
        with colcards[0]:
            st.markdown("**Ta carte**", unsafe_allow_html=True)
            st.markdown(card_html(g["cards"][g["human_seat"]]), unsafe_allow_html=True)
        with colcards[1]:
            st.markdown("**Carte commune**", unsafe_allow_html=True)
            if g["board"] is not None:
                st.markdown(card_html(g["board"]), unsafe_allow_html=True)
            else:
                st.markdown(card_html(0, hidden=True), unsafe_allow_html=True)
        with colcards[2]:
            st.markdown("**Carte du bot**", unsafe_allow_html=True)
            reveal_bot = g["done"]
            st.markdown(card_html(g["cards"][1 - g["human_seat"]], hidden=not reveal_bot),
                        unsafe_allow_html=True)

        pot = g["committed"][0] + g["committed"][1]
        st.markdown(f"<div class='pot-badge'>Pot : {pot} jetons</div>", unsafe_allow_html=True)
        st.write("")

        if g["done"]:
            res = g["result_u_human"]
            if not st.session_state.get("counted_hand_id") == id(g):
                st.session_state.bank += res
                st.session_state.hands += 1
                st.session_state.counted_hand_id = id(g)
            if res > 0:
                st.success(f"Tu gagnes {res:+.0f} jetons.")
            elif res < 0:
                st.error(f"Tu perds {res:+.0f} jetons.")
            else:
                st.info("Pot partage, personne ne gagne.")
        else:
            player = lg.current_player(g)
            if player == g["human_seat"]:
                info = lg.current_infoset(g, g["human_seat"])
                advice = STRATEGY.get(info)
                acts, labels = lg.legal_action_labels(g)

                colL, colR = st.columns([1, 1])
                with colL:
                    st.markdown("**A toi de jouer**")
                    bcols = st.columns(len(acts))
                    for i, a in enumerate(acts):
                        if bcols[i].button(labels[a], key=f"act_{a}_{id(g)}", use_container_width=True):
                            ng = lg.apply_action(g, a)
                            ng = advance_bot(ng)
                            st.session_state.game = ng
                            st.rerun()
                with colR:
                    if advice:
                        st.markdown("**Ce que le solveur jouerait ici**")
                        st.markdown(prob_bars(advice, labels), unsafe_allow_html=True)

        # historique du coup
        if g["log"]:
            with st.expander("Deroule du coup"):
                for line in g["log"]:
                    st.write(line)


# ------------------------- Onglet 4 : comparaison des algos -------------------------

with tab_compare:
    st.markdown("### Trois algorithmes sur le meme jeu")
    st.markdown(
        "Le meme jeu de Leduc, resolu par trois methodes differentes de la famille "
        "CFR. On mesure l'exploitabilite (plus c'est bas, mieux c'est) en fonction "
        "du **nombre de noeuds de jeu visites**, qui reflete le vrai cout de calcul. "
        "Comparer a nombre d'iterations egal serait trompeur, car une iteration de "
        "MCCFR coute bien moins qu'un parcours complet de l'arbre."
    )

    COLORS = {
        "CFR+ (strategie courante)": "#3d9970",
        "CFR classique (moyenne)": "#4a80b4",
        "MCCFR (moyenne)": "#b5651d",
        "CFR+ (moyenne)": "#c0392b",
    }

    rows = []
    for name, pts in VARIANTS.items():
        for p in pts:
            rows.append({"Noeuds visites": p["nodes"],
                         "Exploitabilite": p["exploitability"],
                         "Algorithme": name})
    dfc = pd.DataFrame(rows)

    order = list(COLORS.keys())
    chart = (
        alt.Chart(dfc)
        .mark_line(point=True)
        .encode(
            x=alt.X("Noeuds visites", title="Noeuds de jeu visites (echelle log)",
                    scale=alt.Scale(type="log")),
            y=alt.Y("Exploitabilite", title="Exploitabilite (echelle log)",
                    scale=alt.Scale(type="log")),
            color=alt.Color("Algorithme", scale=alt.Scale(
                domain=order, range=[COLORS[o] for o in order]),
                legend=alt.Legend(orient="bottom", columns=2)),
            tooltip=["Algorithme", "Noeuds visites",
                     alt.Tooltip("Exploitabilite", format=".4f")],
        )
        .properties(height=420)
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("#### Comment lire ce graphe")
    st.markdown(
        "- **CFR+ (strategie courante)** en vert : le meilleur ici. Le CFR+ a la "
        "propriete rare que sa strategie de l'instant converge, pas seulement sa "
        "moyenne.\n"
        "- **CFR classique (moyenne)** en bleu : solide, mais converge plus "
        "lentement.\n"
        "- **CFR+ (moyenne)** en rouge : nettement moins bon que la courante du "
        "CFR+. C'est une vraie subtilite, expliquee dans les notes techniques : la "
        "moyenne devient uniforme sur les situations rares, que la meilleure "
        "reponse exploite.\n"
        "- **MCCFR (moyenne)** en orange : converge plus lentement par noeud sur ce "
        "petit jeu. Sa force n'est pas ici : c'est la seule methode qui passe a "
        "l'echelle sur les tres gros jeux, ou parcourir tout l'arbre est impossible."
    )
    st.caption(f"Budget de calcul : {NODE_BUDGET:,} noeuds visites par algorithme."
               .replace(",", " "))


# ------------------------- Onglet 5 : notes techniques -------------------------

with tab_notes:
    st.markdown("### Ce que le build a reellement appris")
    st.markdown(
        "Ces trois points ne viennent pas d'un tutoriel mais du debug reel. Ils "
        "font la difference entre recopier un algorithme et le comprendre."
    )

    st.markdown("#### 1. Mises a jour simultanees contre alternees")
    st.markdown(
        "Ma premiere version du CFR+ convergeait en 1 sur racine de T, exactement "
        "comme le CFR classique, alors que le CFR+ doit etre plus rapide. La cause : "
        "je mettais a jour les deux joueurs a chaque parcours. Le vrai CFR+ n'en met "
        "qu'un seul par iteration. Apres correction, la convergence a change du tout "
        "au tout."
    )

    st.markdown("#### 2. Strategie moyenne contre strategie courante")
    st.markdown(
        "Le point le plus subtil. En CFR classique, seule la strategie moyenne "
        "converge ; celle de l'instant oscille. En CFR+, la strategie courante "
        "converge aussi, et souvent mieux. J'ai vu la moyenne du CFR+ stagner vers "
        "0.05 pendant que la courante passait sous 0.005. La raison : la moyenne "
        "devient quasi uniforme sur les situations rarement atteintes, et la "
        "meilleure reponse exploite precisement ces trous. La courante, elle, reste "
        "sensee partout grace au regret matching. D'ou le choix d'exporter la "
        "courante. Le graphe de l'onglet precedent montre cet ecart en direct."
    )

    st.markdown("#### 3. Comparer honnetement des algos de cout different")
    st.markdown(
        "Une iteration de MCCFR coute bien moins qu'un parcours complet de l'arbre. "
        "J'ai donc compare en noeuds visites, pas en iterations. Sur un petit jeu, "
        "les methodes a parcours complet gagnent ; l'interet de MCCFR apparait sur "
        "les tres gros jeux. Il a aussi fallu corriger l'accumulation de la moyenne "
        "en MCCFR : elle doit se faire aux noeuds de l'adversaire echantillonne, "
        "sinon elle est biaisee et remonte au lieu de descendre."
    )
