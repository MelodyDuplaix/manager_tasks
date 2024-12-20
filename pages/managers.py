import streamlit as st
import json
import os

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

# Fonction pour mettre à jour l'historique avec le nouveau nom de sous-manager
def update_historique(old_name, new_name, log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open(log_file, 'w', encoding='utf-8') as f:
        for line in lines:
            # Remplacer l'ancien nom par le nouveau dans chaque ligne
            f.write(line.replace(old_name, new_name))

data_file = 'data.json'
log_file = 'historique.csv'
data = load_data(data_file)

# Fonction pour ajouter un nouveau sous-manager
def ajouter_sous_manager(nom):
    if nom not in data['managers']:
        data['managers'][nom] = {
            "objectif": 10,
            "daily": 0,
            "total": 0,
            "objectif_mensuel": 300,
            "objectif_hebdomadaire": 100,
            "taches": {}, 
            "recompenses": {},
            "taches_ponctuelles": {}
        }
        save_data(data_file, data)

# Fonction pour modifier le nom d'un sous-manager existant
def modifier_nom_sous_manager(ancien_nom, nouveau_nom):
    if ancien_nom in data['managers'] and nouveau_nom not in data['managers']:
        data['managers'][nouveau_nom] = data['managers'].pop(ancien_nom)
        save_data(data_file, data)
        update_historique(ancien_nom, nouveau_nom, log_file)  # Mettre à jour l'historique

# Fonction pour supprimer un sous-manager
def supprimer_sous_manager(nom):
    if nom in data['managers']:
        del data['managers'][nom]
        save_data(data_file, data)

st.set_page_config(page_title="Gestion des Sous-managers", page_icon="👥", layout="centered")

st.title("Gestion des Sous-managers")

# Formulaire pour ajouter un nouveau sous-manager
with st.expander("Ajouter un nouveau sous-manager"):
    nom_nouveau_manager = st.text_input("Nom du nouveau sous-manager")
    if st.button("Ajouter sous-manager"):
        ajouter_sous_manager(nom_nouveau_manager)

st.header("Sous-managers existants")

for sous_manager in data.get("managers", {}):
    with st.expander(f"Sous-manager : {sous_manager}"):
        # Formulaire pour modifier le nom du sous-manager
        nouveau_nom = st.text_input("Nouveau nom", value=sous_manager, key=f"nom_{sous_manager}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Modifier le nom", on_click=modifier_nom_sous_manager, args=(sous_manager, nouveau_nom), key=f"modifier_{sous_manager}")
        with col2:
            st.button("Supprimer", on_click=supprimer_sous_manager, args=(sous_manager,), key=f"supprimer_{sous_manager}")
