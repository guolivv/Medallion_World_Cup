import streamlit as st
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
load_dotenv()

st.set_page_config(page_title="Copa do Mundo - Stats", layout="wide")
st.title("Estatísticas da Copa do Mundo")
st.write("Use o menu lateral para navegar entre as páginas.")