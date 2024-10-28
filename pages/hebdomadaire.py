import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime, timedelta

# Fichiers de données
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

# Fonction pour calculer les pièces hebdomadaires pour chaque sous-manager
def calculer_pieces_hebdomadaires(sous_manager):
    if os.path.exists(historique_file):
        df = pd.read_csv(historique_file, header=None, names=["date", "manager", "type", "nom", "valeur"])
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y %H:%M:%S')

        debut_semaine = (datetime.now() - timedelta(days=datetime.now().weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        df_semaine = df[(df['date'] >= debut_semaine) & (df['manager'] == sous_manager)]

        total_taches = df_semaine[df_semaine['type'] == "Tâche"]['valeur'].sum()
        total_recompenses = df_semaine[df_semaine['type'] == "Récompense"]['valeur'].sum()
        total_hebdomadaire = total_taches - total_recompenses
        return total_hebdomadaire

    return 0

st.set_page_config(page_title="Progression hebdomadaire", page_icon="📊", layout="centered")

data = load_data(data_file)

st.title("Suivi des pièces hebdomadaires")

# Boucle sur chaque sous-manager pour afficher leur progression hebdomadaire
for sous_manager, sous_manager_data in data.get("managers", {}).items():
    st.subheader(f"Progression de {sous_manager}")
    
    objectif_hebdomadaire = sous_manager_data.get('objectif_hebdomadaire', 50)  # Par défaut 50
    
    pieces_hebdomadaires = calculer_pieces_hebdomadaires(sous_manager)
    
    st.write(f"Nombre de pièces accumulées cette semaine : {pieces_hebdomadaires}")
    st.write(f"Objectif hebdomadaire : {objectif_hebdomadaire} pièces")
    
    progression = int(pieces_hebdomadaires) / objectif_hebdomadaire if objectif_hebdomadaire > 0 else 0
    st.progress(max(0.00, min(1.00, progression)))
    
    # Formulaire pour modifier l'objectif hebdomadaire du sous-manager
    with st.expander(f"Modifier l'objectif de {sous_manager}"):
        with st.form(f"modifier_objectif_{sous_manager}"):
            nouvel_objectif = st.number_input(
                "Nouvel objectif hebdomadaire", 
                min_value=1, 
                step=1, 
                value=objectif_hebdomadaire, 
                key=f"objectif_{sous_manager}"
            )
            submit = st.form_submit_button("Modifier l'objectif")

            if submit:
                sous_manager_data['objectif_hebdomadaire'] = nouvel_objectif
                data["managers"][sous_manager] = sous_manager_data
                save_data(data_file, data)
                st.success(f"Objectif hebdomadaire de {sous_manager} mis à jour à {nouvel_objectif} pièces")
                st.rerun()
