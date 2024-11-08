import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

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

# Fonction pour calculer les pièces mensuelles pour chaque sous-manager
def calculer_pieces_mensuelles(sous_manager):
    if os.path.exists(historique_file):
        df = pd.read_csv(historique_file, header=None, names=["date", "manager", "type", "nom", "valeur"])
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y %H:%M:%S')

        mois_courant = datetime.now().month
        annee_courante = datetime.now().year
        df_mois = df[(df['date'].dt.month == mois_courant) & 
                     (df['date'].dt.year == annee_courante) &
                     (df['manager'] == sous_manager)]

        total_taches = df_mois[df_mois['type'] == "Tâche"]['valeur'].sum()
        return total_taches

    return 0

st.set_page_config(page_title="Progression mensuelle", page_icon="📊", layout="centered")

data = load_data(data_file)

st.title("Suivi des pièces mensuelles")

# Boucle sur chaque sous-manager pour afficher leur progression
for sous_manager, sous_manager_data in data.get("managers", {}).items():
    st.subheader(f"Progression de {sous_manager}")
    
    objectif_mensuel = sous_manager_data.get('objectif_mensuel', 100)  # Par défaut 100
    
    pieces_mensuelles = calculer_pieces_mensuelles(sous_manager)
    
    st.write(f"Nombre de pièces accumulées ce mois-ci : {pieces_mensuelles}")
    st.write(f"Objectif mensuel : {objectif_mensuel} pièces")
    
    progression = int(pieces_mensuelles) / objectif_mensuel if objectif_mensuel > 0 else 0
    st.progress(max(0.00, min(1.00, progression)))
    
    with st.expander(f"Modifier l'objectif de {sous_manager}"):
        with st.form(f"modifier_objectif_{sous_manager}"):
            nouvel_objectif = st.number_input(
                "Nouvel objectif mensuel", 
                min_value=1, 
                step=1, 
                value=objectif_mensuel, 
                key=f"objectif_{sous_manager}"
            )
            submit = st.form_submit_button("Modifier l'objectif")

            if submit:
                sous_manager_data['objectif_mensuel'] = nouvel_objectif
                data["managers"][sous_manager] = sous_manager_data
                save_data(data_file, data)
                st.success(f"Objectif mensuel de {sous_manager} mis à jour à {nouvel_objectif} pièces")
                st.rerun()
