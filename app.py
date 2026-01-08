import streamlit as st
import pandas as pd
from datetime import date

# --------------------
# CONFIG
# --------------------
st.set_page_config(page_title="PoM Simulator", layout="centered")

st.title("🧠 PoM – Simulateur de règles de scoring")
st.caption("MVP pédagogique – Données fictives et anonymisées")

# --------------------
# CONTEXTE
# --------------------
st.markdown("### 📅 Situation analysée")

reporting_date = date.today().strftime("%d/%m/%Y")
st.write(f"Date du reporting analysé : **{reporting_date}**")

st.caption(
    "Cette analyse correspond à la situation la plus récente du rapport risque transmis."
)

# KPI initiaux (issus de l’email d’alerte – décimales converties en %)
base_accept = 20   # %
base_refusal = 80  # %

st.markdown("### 📊 Indicateurs clés – Situation du jour")

col1, col2 = st.columns(2)
col1.metric("✅ Taux d’acceptation", f"{base_accept} %")
col2.metric("❌ Taux de refus", f"{base_refusal} %")

# Message pédagogique aligné avec le prompt
st.info(
    f"Aujourd’hui, le taux d’acceptation est de **{base_accept}%**, alors que nous "
    "visons habituellement une plage comprise entre **25% et 35%**. "
    "Cela signifie que nous acceptons moins de dossiers que prévu, ce qui peut "
    "réduire le volume de clients financés."
)

# --------------------
# RÈGLES DE SCORING
# --------------------
st.markdown("### 🎯 Règles de scoring recommandées")

st.caption(
    "Suite à l’alerte, certaines règles ont été identifiées comme prioritaires. "
    "Elles sont **pré-paramétrées** ci-dessous. Vous pouvez les ajuster avant validation."
)

rules = {
    "RISK_SCORE_HIGH": {
        "impact": 4,
        "description": "Seuil strict sur le score de risque client"
    },
    "DEBT_RATIO": {
        "impact": 3,
        "description": "Règle limitant le taux d’endettement"
    },
    "AGE_CLIENT": {
        "impact": 2,
        "description": "Restriction liée à l’âge du client"
    },
    "STABILITY_EMPLOYMENT": {
        "impact": 1,
        "description": "Ancienneté minimale dans l’emploi"
    }
}

selected_rules = {}

for rule, data in rules.items():
    selected_rules[rule] = st.checkbox(
        f"{rule} – {data['description']} (impact estimé -{data['impact']} pts d’acceptation)",
        value=True  # pré-sélection = cohérent avec l’email
    )

# --------------------
# SIMULATION
# --------------------
st.markdown("---")

if st.button("🔍 Simuler l’impact des ajustements"):
    impact_total = sum(
        data["impact"]
        for rule, data in rules.items()
        if selected_rules[rule]
    )

    new_accept = max(base_accept - impact_total, 0)
    new_refusal = min(base_refusal + impact_total, 100)

    st.markdown("### 📈 Résultat de la simulation")

    col1, col2 = st.columns(2)
    col1.metric(
        "Nouveau taux d’acceptation",
        f"{new_accept} %",
        delta=f"{new_accept - base_accept} pts"
    )
    col2.metric(
        "Nouveau taux de refus",
        f"{new_refusal} %",
        delta=f"{new_refusal - base_refusal} pts"
    )

    # Graphique comparatif
    df = pd.DataFrame({
        "Indicateur": ["Acceptation", "Refus"],
        "Situation actuelle": [base_accept, base_refusal],
        "Après ajustement": [new_accept, new_refusal]
    }).set_index("Indicateur")

    st.bar_chart(df)

    st.success(
        "Simulation terminée. "
        "Cette projection permet d’évaluer rapidement l’impact métier avant toute décision."
    )

# --------------------
# VALIDATION (FICTIVE)
# --------------------
st.markdown("---")

st.markdown("### 🚀 Passer à l’action")

st.caption(
    "Les règles sont déjà configurées selon la recommandation. "
    "Vous gardez le contrôle final sur toute modification."
)

if st.button("✅ Accéder aux règles pré-configurées"):
    st.info(
        "Action simulée : les règles sélectionnées seraient transmises à l’outil PoM "
        "pour validation humaine et mise en production."
    )


