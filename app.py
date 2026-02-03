import streamlit as st 
import time
import sys

from src.toy_factory.factory import Factory
from src.toy_factory.product import Product
from src.utils.logger import config_logging


sys.path.append(".")

if "factory" not in st.session_state:
    st.session_state.factory = None
    
if "simulation_done" not in st.session_state:
    st.session_state.simulation_done = False

tab_simulation, tab_analysis, tab_data = st.tabs( ["▶️ Simulation", "📊 Analyse", "📁 Données"])

st.set_page_config(page_title="Toy Factory Simulator", layout="wide")

logger = config_logging()

def run_simulation(production_rate, time_scale, duration, logger):
    usine = Factory(logger, production_rate, time_scale)

    delta_time = 0.1
    remaining_time = duration

    while remaining_time > 0:
        usine.update(delta_time)
        remaining_time -= delta_time

    return usine

@st.cache_resource
def cached_simulation(production_rate, time_scale, duration):
    return run_simulation(production_rate, time_scale, duration, logger)

st.set_page_config(page_title="🏭 Toy Factory Simulator",layout="wide")

st.title("🏭 Toy Factory Simulator")
st.caption(
    "Simulation d'une usine de fabrication de jouets — analyse de la production et "
    "goulots d’étranglement."
)


# 🎛️ Paramètres utilisateur
st.sidebar.header("Paramètres de simulation")

production_rate = st.sidebar.slider(
    "Rendement (produits / seconde)",
    min_value=0.1,
    max_value=2.0,
    value=0.5,
    step=0.1
)

time_scale = st.sidebar.slider(
    "Accélération du temps",
    min_value=1,
    max_value=50,
    value=10
)

simulation_duration = st.sidebar.slider(
    "Durée de simulation (secondes réelles)",
    min_value=5,
    max_value=60,
    value=10
)

with tab_simulation:
    st.header("▶️ Pilotage de la simulation")
    st.markdown(
        """
        Configurez les paramètres de production puis lancez la simulation.
        Le moteur simule un flux de production avec pannes de stations, défauts et reprises de produits.
        """
    )

    if st.button("Lancer la simulation"):
        with st.spinner("Simulation en cours..."):
            usine = cached_simulation(production_rate, time_scale, simulation_duration)

        st.session_state.factory = usine
        st.session_state.simulation_done = True
        st.success("Simulation terminée")

    if st.session_state.simulation_done:
        usine = st.session_state.factory

        st.subheader("📊 Indicateurs clés")

        col1, col2, col3 = st.columns(3)
        col1.metric("Produits créés", Product.SERIAL_NUMBER)
        col2.metric("Produits finis", len(usine.finished_products))
        col3.metric("Produits rejetés", len(usine.rejected_products))


with tab_analysis:
    st.header("📊 Analyse de performance")

    if not st.session_state.simulation_done:
        st.warning("Aucune donnée disponible. Lancez une simulation.")
    else:
        usine = st.session_state.factory
        utilization = usine.compute_station_utilization()

        st.subheader("Taux d’occupation des stations")
        st.bar_chart(utilization)

        bottleneck = max(utilization, key=utilization.get)
        st.error(
            f"🔴 Goulot d’étranglement principal : **{bottleneck.capitalize()}**"
        )







