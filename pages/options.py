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
def ajouter_nouvelle_tache(sous_manager, nom, valeur, sous_type):
    data['managers'][sous_manager]['taches'][nom] = (valeur, sous_type)
    save_data(data_file, data)
    st.rerun()

# Fonction pour modifier une tâche existante
def modifier_tache(sous_manager, ancien_nom, nouveau_nom, nouvelle_valeur, nouveau_sous_type):
    if ancien_nom in data['managers'][sous_manager]['taches']:
        del data['managers'][sous_manager]['taches'][ancien_nom]
    data['managers'][sous_manager]['taches'][nouveau_nom] = (nouvelle_valeur, nouveau_sous_type)
    save_data(data_file, data)
    st.rerun()

# Fonction pour supprimer une tâche
def supprimer_tache(sous_manager, nom):
    if nom in data['managers'][sous_manager]['taches']:
        del data['managers'][sous_manager]['taches'][nom]
        save_data(data_file, data)

# Fonction pour ajouter une nouvelle récompense
def ajouter_nouvelle_recompense(sous_manager, nom, valeur):
    data['managers'][sous_manager]['recompenses'][nom] = valeur
    save_data(data_file, data)
    st.rerun()

# Fonction pour modifier une récompense existante
def modifier_recompense(sous_manager, ancien_nom, nouveau_nom, nouvelle_valeur):
    if ancien_nom in data['managers'][sous_manager]['recompenses']:
        del data['managers'][sous_manager]['recompenses'][ancien_nom]
    data['managers'][sous_manager]['recompenses'][nouveau_nom] = nouvelle_valeur
    save_data(data_file, data)
    st.rerun()

# Fonction pour supprimer une récompense
def supprimer_recompense(nom):
    if nom in data['recompenses']:
        del data['recompenses'][nom]
        save_data(data_file, data)

# Fonction pour modifier l'objectif
def modifier_objectif(sous_manager, nouvel_objectif):
    data['managers'][sous_manager]['objectif_quotidien'] = nouvel_objectif
    save_data(data_file, data)

st.set_page_config(page_title="Modification des tâches et récompenses", page_icon="⚙️", layout="centered")

st.title("Modification des Tâches, Récompenses et Objectif")

sous_manager = st.sidebar.selectbox("Choisissez le sous-manager", options=list(data.get("managers", {}).keys()))

# Section pour l'objectif
st.header(f"Objectif quotidien de {sous_manager}")
objectif = data["managers"][sous_manager].get('objectif_quotidien', 0)
nouvel_objectif = st.number_input("Modifier l'objectif", value=objectif, step=1)
if st.button("Mettre à jour l'objectif"):
    modifier_objectif(sous_manager, nouvel_objectif)

# Section pour les tâches
st.header("Tâches")

# Afficher et modifier les tâches existantes pour le sous-manager sélectionné
for tache, (valeur, sous_type) in data["managers"][sous_manager].get("taches", {}).items():
    with st.expander(f"{tache} (valeur: {valeur}, sous-type: {sous_type})"):
        nouveau_nom = st.text_input("Nouveau nom", value=tache, key=f"nom_{tache}_{sous_manager}")
        nouvelle_valeur = st.number_input("Nouvelle valeur", value=valeur, step=1, key=f"valeur_{tache}_{sous_manager}")
        nouveau_sous_type = st.text_input("Nouveau sous-type", value=sous_type, key=f"sous_type_{tache}_{sous_manager}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Modifier", on_click=modifier_tache, args=(sous_manager, tache, nouveau_nom, nouvelle_valeur, nouveau_sous_type), key=f"modifier_{tache}_{sous_manager}")
        with col2:
            st.button("Supprimer", on_click=supprimer_tache, args=(sous_manager, tache), key=f"supprimer_{tache}_{sous_manager}")

# Formulaire pour ajouter une nouvelle tâche pour le sous-manager
with st.expander("Ajouter une nouvelle tâche"):
    nom_tache = st.text_input("Nom de la tâche", key=f"ajouter_nom_{sous_manager}")
    valeur_tache = st.number_input("Valeur de la tâche", min_value=0, step=1, key=f"ajouter_valeur_{sous_manager}")
    sous_type_tache = st.text_input("Sous-type de la tâche", key=f"ajouter_sous_type_{sous_manager}")
    if st.button("Ajouter tâche"):
        ajouter_nouvelle_tache(sous_manager, nom_tache, valeur_tache, sous_type_tache)

# Section pour les récompenses
st.header("Récompenses")

# Afficher et modifier les récompenses existantes pour le sous-manager sélectionné
for recompense, valeur in data["managers"][sous_manager].get("recompenses", {}).items():
    with st.expander(f"{recompense} (valeur: {valeur})"):
        nouveau_nom = st.text_input("Nouveau nom", value=recompense, key=f"nom_{recompense}_{sous_manager}")
        nouvelle_valeur = st.number_input("Nouvelle valeur", value=valeur, step=1, key=f"valeur_{recompense}_{sous_manager}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Modifier", on_click=modifier_recompense, args=(sous_manager, recompense, nouveau_nom, nouvelle_valeur), key=f"modifier_{recompense}_{sous_manager}")
        with col2:
            st.button("Supprimer", on_click=supprimer_recompense, args=(sous_manager, recompense), key=f"supprimer_{recompense}_{sous_manager}")

# Formulaire pour ajouter une nouvelle récompense pour le sous-manager
with st.expander("Ajouter une nouvelle récompense"):
    nom_recompense = st.text_input("Nom de la récompense", key=f"ajouter_recompense_nom_{sous_manager}")
    valeur_recompense = st.number_input("Valeur de la récompense", min_value=0, step=1, key=f"ajouter_recompense_valeur_{sous_manager}")
    if st.button("Ajouter récompense"):
        ajouter_nouvelle_recompense(sous_manager, nom_recompense, valeur_recompense)
