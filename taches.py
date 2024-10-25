import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime

# Fonction pour charger les données depuis le fichier JSON
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:  # Spécifiez l'encodage UTF-8
            return json.load(f)
    return {}

# Fonction pour sauvegarder les données dans le fichier JSON
def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:  # Spécifiez l'encodage UTF-8
        json.dump(data, f, ensure_ascii=False, indent=4)

# Fonction pour enregistrer l'action dans un fichier CSV
def log_action(filename, action_type, name, value):
    with open(filename, 'a', encoding='utf-8') as f:  # Spécifiez l'encodage UTF-8
        f.write(f"{datetime.now().strftime('%d/%m/%y %H:%M:%S')},{action_type},{name},{value}\n")

# Formatage de la page avec CSS
def formatage_de_la_page(fichier_css):
    with open(fichier_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Chargement des données depuis le fichier JSON
data_file = 'data.json'
data = load_data(data_file)

# Initialisation des listes de tâches et récompenses si elles n'existent pas
if 'taches' not in data:
    data['taches'] = {
        "Faire une liste de 5 nom": (1, "Administration"),
        "Appeler": (2, "Communication"),
        "Caler une date de rdv": (2, "Planification"),
        "Créer une fiche": (1, "Administration"),
        "Appeler les recommandations de ses clients": (2, "Communication"),
        "Amener une dégustation": (2, "Vente"),
        "Vente faite": (5, "Vente")
    }

if 'recompenses' not in data:
    data['recompenses'] = {
        "jours de repos": 20
    }

# Sauvegarde des données mises à jour
save_data(data_file, data)

st.set_page_config(
    page_title="Manager",
    page_icon="✅",
    layout="wide"
)

formatage_de_la_page("style.css")

contexte = "Manager de taches test / Première version"
log_file = 'historique.csv'  # Fichier pour l'historique

# Initialisation des variables pour objectif, daily et total
if 'objectif' not in data:
    data['objectif'] = 10
if 'daily' not in data:
    data['daily'] = 0
if 'total' not in data:
    data['total'] = 0

st.session_state.objectif = data['objectif']
st.session_state.daily = data['daily']
st.session_state.total = data['total']

col_blank, col_general = st.columns([1, 10])
with col_general:
    st.title("Manager")
    st.write(contexte)

    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown(f"<div class='total_metric'><p class='label_total'>Solde:</p><p class='value_total'>{st.session_state.total}</p></div>", unsafe_allow_html=True)

    st.header("Objectifs")
    col_progress, col_metric = st.columns([1, 3])

    with col_metric:
        st.metric(label="Daily", value=f"{st.session_state.daily} / {st.session_state.objectif}")

    with col_progress:
        progress_value = int(min(100, max(0, (100 * st.session_state.daily) / st.session_state.objectif)))
        my_bar = st.progress(progress_value)

    def reset_daily():
        st.session_state.daily = 0
        data['daily'] = 0
        save_data(data_file, data)

    st.button("Commencer la journée", key="start_day", on_click=reset_daily, type="secondary")

    def retirer_recompense(valeur, recompense):
        st.session_state.total = st.session_state.total - valeur
        data['total'] = st.session_state.total
        save_data(data_file, data)
        log_action(log_file, "Récompense", recompense, valeur)

    def ajouter_tache(valeur, nom_tache):
        st.session_state.total = st.session_state.total + valeur
        st.session_state.daily = st.session_state.daily + valeur
        data['daily'] = st.session_state.daily
        data['total'] = st.session_state.total
        save_data(data_file, data)
        log_action(log_file, "Tâche", nom_tache, valeur)

    st.header("Récompenses")
    for recompense, valeur in data['recompenses'].items():
        st.button(f"{recompense} (-{valeur})", on_click=retirer_recompense, args=(valeur, recompense))

    st.header("Tâches")

    sous_types = {}
    for tache, (valeur, sous_type) in data['taches'].items():
        if sous_type not in sous_types:
            sous_types[sous_type] = []
        sous_types[sous_type].append((tache, valeur))

    col_sous_types = st.columns(len(sous_types))
    for idx, (sous_type, taches) in enumerate(sous_types.items()):
        with col_sous_types[idx]:
            st.subheader(sous_type)
            for tache, valeur in taches:
                st.button(f"{tache} (+{valeur})", on_click=ajouter_tache, args=(valeur, tache))
