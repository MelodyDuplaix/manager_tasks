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

# Chargement des données depuis le fichier JSON
data_file = 'data.json'
data = load_data(data_file)

# Fonction pour ajouter une nouvelle tâche
def ajouter_nouvelle_tache(nom, valeur, sous_type):
    data['taches'][nom] = (valeur, sous_type)
    save_data(data_file, data)
    st.experimental_rerun()

# Fonction pour modifier une tâche existante
def modifier_tache(ancien_nom, nouveau_nom, nouvelle_valeur, nouveau_sous_type):
    if ancien_nom in data['taches']:
        del data['taches'][ancien_nom]
    data['taches'][nouveau_nom] = (nouvelle_valeur, nouveau_sous_type)
    save_data(data_file, data)
    st.experimental_rerun()

# Fonction pour supprimer une tâche
def supprimer_tache(nom):
    if nom in data['taches']:
        del data['taches'][nom]
        save_data(data_file, data)

# Fonction pour ajouter une nouvelle récompense
def ajouter_nouvelle_recompense(nom, valeur):
    data['recompenses'][nom] = valeur
    save_data(data_file, data)
    st.experimental_rerun()

# Fonction pour modifier une récompense existante
def modifier_recompense(ancien_nom, nouveau_nom, nouvelle_valeur):
    if ancien_nom in data['recompenses']:
        del data['recompenses'][ancien_nom]
    data['recompenses'][nouveau_nom] = nouvelle_valeur
    save_data(data_file, data)
    st.experimental_rerun()

# Fonction pour supprimer une récompense
def supprimer_recompense(nom):
    if nom in data['recompenses']:
        del data['recompenses'][nom]
        save_data(data_file, data)

# Fonction pour modifier l'objectif
def modifier_objectif(nouvel_objectif):
    data['objectif'] = nouvel_objectif
    save_data(data_file, data)

st.set_page_config(page_title="Modification des tâches et récompenses", page_icon="⚙️", layout="centered")

st.title("Modifier, Ajouter et Supprimer des Tâches, Récompenses et Objectif quotidien")

# Section pour l'objectif
st.header("Objectif quotidien")

# Afficher et modifier l'objectif
objectif = data.get('objectif', 0)  # Récupérer l'objectif actuel ou 0 s'il n'existe pas
nouvel_objectif = st.number_input("Modifier l'objectif", value=objectif, step=1)
if st.button("Mettre à jour l'objectif"):
    modifier_objectif(nouvel_objectif)

# Section pour les tâches
st.header("Tâches")

# Afficher et modifier les tâches existantes
for tache, (valeur, sous_type) in data['taches'].items():
    with st.expander(f"{tache} (valeur: {valeur}, sous-type: {sous_type})"):
        nouveau_nom = st.text_input("Nouveau nom", value=tache, key=f"nom_{tache}")
        nouvelle_valeur = st.number_input("Nouvelle valeur", value=valeur, step=1, key=f"valeur_{tache}")  
        nouveau_sous_type = st.text_input("Nouveau sous-type", value=sous_type, key=f"sous_type_{tache}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Modifier", on_click=modifier_tache, args=(tache, nouveau_nom, nouvelle_valeur, nouveau_sous_type), key=f"modifier_{tache}")
        with col2:
            st.button("Supprimer", on_click=supprimer_tache, args=(tache,), key=f"supprimer_{tache}")

# Formulaire pour ajouter une nouvelle tâche
with st.expander("Ajouter une nouvelle tâche"):
    nom_tache = st.text_input("Nom de la tâche")
    valeur_tache = st.number_input("Valeur de la tâche", min_value=0, step=1)
    sous_type_tache = st.text_input("Sous-type de la tâche")
    if st.button("Ajouter tâche"):
        ajouter_nouvelle_tache(nom_tache, valeur_tache, sous_type_tache)

# Section pour les récompenses
st.header("Récompenses")

# Afficher et modifier les récompenses existantes
for recompense, valeur in data['recompenses'].items():
    with st.expander(f"{recompense} (valeur: {valeur})"):
        nouveau_nom = st.text_input("Nouveau nom", value=recompense, key=f"nom_{recompense}")
        nouvelle_valeur = st.number_input("Nouvelle valeur", value=valeur, step=1, key=f"valeur_{recompense}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Modifier", on_click=modifier_recompense, args=(recompense, nouveau_nom, nouvelle_valeur), key=f"modifier_{recompense}")
        with col2:
            st.button("Supprimer", on_click=supprimer_recompense, args=(recompense,), key=f"supprimer_{recompense}")

# Formulaire pour ajouter une nouvelle récompense
with st.expander("Ajouter une nouvelle récompense"):
    nom_recompense = st.text_input("Nom de la récompense")
    valeur_recompense = st.number_input("Valeur de la récompense", min_value=0, step=1)
    if st.button("Ajouter récompense"):
        ajouter_nouvelle_recompense(nom_recompense, valeur_recompense)
