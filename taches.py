import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime

# Fonction pour charger les données depuis le fichier JSON
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Fonction pour sauvegarder les données dans le fichier JSON
def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Fonction pour enregistrer l'action dans un fichier CSV
def log_action(filename, manager, action_type, name, value):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().strftime('%d/%m/%y %H:%M:%S')},{manager},{action_type},{name},{value}\n")

# Formatage de la page avec CSS
def formatage_de_la_page(fichier_css):
    with open(fichier_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

data_file = 'data.json'
log_file = 'historique.csv'

data = load_data(data_file)

st.set_page_config(
    page_title="Manager",
    page_icon="✅",
    layout="wide"
)

formatage_de_la_page("style.css")

sous_manager_selection = st.sidebar.selectbox("Sélectionnez un sous-manager", list(data.get("managers", {}).keys()))

# Charger les données spécifiques au sous-manager sélectionné
sous_manager_data = data["managers"].get(sous_manager_selection, {})
st.session_state.objectif = sous_manager_data.get("objectif", 10)
st.session_state.daily = sous_manager_data.get("daily", 0)
st.session_state.total = sous_manager_data.get("total", 0)

col_blank, col_general = st.columns([1, 10])
with col_general:
    st.title(f"Manager : {sous_manager_selection}")
    st.write(f"Gestion des tâches et récompenses pour {sous_manager_selection}")

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
        sous_manager_data['daily'] = 0
        save_data(data_file, data)

    st.button("Commencer la journée", key="start_day", on_click=reset_daily, type="secondary")

    def retirer_recompense(valeur, recompense):
        st.session_state.total -= valeur
        sous_manager_data['total'] = st.session_state.total
        save_data(data_file, data)
        log_action(log_file, sous_manager_selection, "Récompense", recompense, valeur)

    def ajouter_tache(valeur, nom_tache, tache_ponctuelle=False):
        st.session_state.total += valeur
        st.session_state.daily += valeur
        sous_manager_data['daily'] = st.session_state.daily
        sous_manager_data['total'] = st.session_state.total
        save_data(data_file, data)
        log_action(log_file, sous_manager_selection, "Tâche", nom_tache, valeur)
        # Supprimer la tâche ponctuelle après l'exécution
        if tache_ponctuelle:
            del sous_manager_data['taches_ponctuelles'][nom_tache]
            save_data(data_file, data)

    st.header("Récompenses")
    for recompense, valeur in sous_manager_data.get('recompenses', {}).items():
        st.button(f"{recompense} (-{valeur})", on_click=retirer_recompense, args=(valeur, recompense))

    st.header("Tâches")

    # Gestion des tâches récurrentes
    sous_types = {}
    for tache, (valeur, sous_type) in sous_manager_data.get('taches', {}).items():
        if sous_type not in sous_types:
            sous_types[sous_type] = []
        sous_types[sous_type].append((tache, valeur))

    col_sous_types = st.columns(len(sous_types))
    for idx, (sous_type, taches) in enumerate(sous_types.items()):
        with col_sous_types[idx]:
            st.subheader(sous_type)
            for tache, valeur in taches:
                st.button(f"{tache} (+{valeur})", on_click=ajouter_tache, args=(valeur, tache))

    # Gestion des tâches ponctuelles
    st.header("Tâches Ponctuelles")

    # Afficher les tâches ponctuelles existantes
    for tache, valeur in sous_manager_data.get('taches_ponctuelles', {}).items():
        st.button(f"{tache} (+{valeur})", on_click=ajouter_tache, args=(valeur, tache, True))

    # Formulaire pour ajouter une nouvelle tâche ponctuelle
    with st.expander("Ajouter une tâche ponctuelle"):
        nom_tache_ponctuelle = st.text_input("Nom de la tâche ponctuelle")
        valeur_tache_ponctuelle = st.number_input("Valeur de la tâche ponctuelle", min_value=0, step=1)
        if st.button("Ajouter tâche ponctuelle"):
            sous_manager_data.setdefault('taches_ponctuelles', {})[nom_tache_ponctuelle] = valeur_tache_ponctuelle
            save_data(data_file, data)
            st.rerun()
