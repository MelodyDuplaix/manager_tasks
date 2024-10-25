import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# Fichier de données
data_file = 'data.json'
historique_file = 'historique.csv'

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

# Fonction pour calculer les pièces accumulées pour le mois en cours
def calculer_pieces_mensuelles():
    if os.path.exists(historique_file):
        # Chargement du fichier CSV avec les colonnes : date, type, nom, valeur
        df = pd.read_csv(historique_file, header=None, names=["date", "type", "nom", "valeur"])
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y %H:%M:%S')

        # Filtrage pour les enregistrements du mois en cours
        mois_courant = datetime.now().month
        annee_courante = datetime.now().year
        df_mois = df[(df['date'].dt.month == mois_courant) & (df['date'].dt.year == annee_courante)]

        # Séparation des types de transactions et calcul des totaux
        total_taches = df_mois[df_mois['type'] == "Tâche"]['valeur'].sum()  # Somme des tâches
        total_recompenses = df_mois[df_mois['type'] == "Récompense"]['valeur'].sum()  # Somme des récompenses

        # Calcul du total net : ajout des tâches, retrait des récompenses
        total_mensuel = total_taches - total_recompenses
        return total_mensuel

    return 0

st.set_page_config(page_title="Progression mensuelle", page_icon="📊", layout="centered")

# Chargement des données
data = load_data(data_file)

# Récupération de l'objectif mensuel depuis data.json
objectif_mensuel = data.get('objectif_mensuel', 100)  # Par défaut, on met un objectif de 100

# Calcul des pièces pour le mois en cours
pieces_mensuelles = calculer_pieces_mensuelles()

# Affichage de la barre de progression
st.title("Suivi des pièces mensuelles")

st.write(f"Nombre de pièces accumulées ce mois-ci : {pieces_mensuelles}")
st.write(f"Objectif mensuel : {objectif_mensuel} pièces")

# Calcul du pourcentage de progression
progression = int(pieces_mensuelles) / objectif_mensuel if objectif_mensuel > 0 else 0
st.progress(max( 0.00 ,min( 1.00, progression)))

# Formulaire pour modifier l'objectif mensuel
with st.form("modifier_objectif"):
    nouvel_objectif = st.number_input("Nouvel objectif mensuel", min_value=1, step=1, value=objectif_mensuel)
    submit = st.form_submit_button("Modifier l'objectif")

    if submit:
        # Mise à jour de l'objectif dans le fichier JSON
        data['objectif_mensuel'] = nouvel_objectif
        save_data(data_file, data)
        st.success(f"Objectif mensuel mis à jour à {nouvel_objectif} pièces")
        st.rerun()
