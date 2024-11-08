import streamlit as st
import pandas as pd
import datetime
import os
import json

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

log_file = 'historique.csv'
data_file = 'data.json'
data = load_data(data_file)

st.set_page_config(page_title="Historique des tâches", page_icon="📚", layout="centered")

def formatage_de_la_page(fichier_css):
    with open(fichier_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

formatage_de_la_page("style.css")

st.title("Historique des tâches")



historique = pd.read_csv(log_file, header=None, names=["date", "manager", "type", "nom", "valeur"])
historique['date'] = pd.to_datetime(historique['date'], format='%d/%m/%y %H:%M:%S')

historique.sort_values(by="date", ascending=False, inplace=True)


today = datetime.datetime.now()
next_year = today.year + 1
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

col1, col2 = st.columns([1, 2])
with col1:
    d = st.date_input("Filtrer par date", value=[today, today], format="DD/MM/YYYY")
with col2:
    managers = data.get("managers", {})
    manager_options = list(managers.keys())

    selection = st.segmented_control(
        "Manager", manager_options, selection_mode="multi"
    )

if len(d) == 1:
    d = (d[0], d[0])
historique_filtre = historique[historique['date'].dt.date.between(d[0], d[1])]

if len(selection) > 0:  
    historique_filtre = historique_filtre[historique_filtre['manager'].isin(selection)]

st.dataframe(historique_filtre, height=(len(historique_filtre) + 1) * 35 + 3, hide_index=True, use_container_width=False, width=800)

st.markdown("<p class='label_total'>Total de pièces filtrés<br><span id='total_historique'>" + str(len(historique_filtre)) + "<span></p>", unsafe_allow_html=True)