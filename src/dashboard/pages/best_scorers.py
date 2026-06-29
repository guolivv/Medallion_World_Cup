import streamlit as st
from src.dashboard.data.queries import get_top_scorers

st.title("Artilheiros")

df = get_top_scorers()
st.dataframe(df)