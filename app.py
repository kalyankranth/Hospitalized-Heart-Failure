import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(
    page_title="Heart Failure Dashboard",
    layout="wide"
)

# Title
st.title("🏥 Hospitalized Heart Failure Dashboard")

# Load Excel
@st.cache_data
def load_data():
    file_path = "data/Cardiacfailure_cleaned.xlsx" 
    xls = pd.ExcelFile(file_path) 

    Demog = pd.read_excel(xls, "Demography")
    HosDis = pd.read_excel(xls, "Hospitalization_Discharge")

    return Demog, HosDis


Demog, HosDis = load_data()

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Demographics", "Hospital Discharge"]
)

# ---------------- DEMOGRAPHICS ---------------- #

if page == "Demographics":

    st.header("👥 Demographics")

    st.dataframe(Demog.head(20))

    st.success("Demographics data loaded ✔️")


# ---------------- DISCHARGE ---------------- #

elif page == "Hospital Discharge":

    st.header("📋 Hospital Discharge")

    st.dataframe(HosDis.head(20))

    st.success("Discharge data loaded ✔️")
