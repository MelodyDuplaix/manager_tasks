import streamlit as st
import pandas as pd
import datetime

log_file = 'historique.csv'

st.set_page_config(page_title="Historique des tâches", page_icon="📚", layout="centered")

# Formatage de la page avec CSS
def formatage_de_la_page(fichier_css):
    with open(fichier_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

formatage_de_la_page("style.css")

st.title("Historique des tâches")

# Charger l'historique des tâches depuis le fichier CSV
historique = pd.read_csv(log_file, header=None, names=["date", "manager", "type", "nom", "valeur"])
historique['date'] = pd.to_datetime(historique['date'], format='%d/%m/%y %H:%M:%S')

# Trier l'historique selon la date ascendante
historique.sort_values(by="date", ascending=False, inplace=True)


today = datetime.datetime.now()
next_year = today.year + 1
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

d = st.date_input("Filtrer par date", value=[today, today], format="DD/MM/YYYY")
if len(d) == 1:
    d = (d[0], d[0])
historique_filtre = historique[historique['date'].dt.date.between(d[0], d[1])]

# Afficher l'historique des tâches
st.dataframe(historique_filtre, height=(len(historique_filtre) + 1) * 35 + 3, hide_index=True, use_container_width=False, width=800)

