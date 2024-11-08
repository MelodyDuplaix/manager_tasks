import streamlit as st
import pandas as pd

log_file = 'historique.csv'

st.set_page_config(page_title="Historique des tâches", page_icon="📚", layout="centered")

st.title("Historique des tâches")

# Charger l'historique des tâches depuis le fichier CSV
historique = pd.read_csv(log_file, header=None, names=["date", "manager", "type", "nom", "valeur"])
historique['date'] = pd.to_datetime(historique['date'], format='%d/%m/%y %H:%M:%S')

# Afficher l'historique des tâches
st.dataframe(historique, height=(len(historique) + 1) * 35 + 3)