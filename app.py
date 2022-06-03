import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard", layout ="wide")

# SideBar
with st.sidebar:
    lg = st.container()
    lg.image("logo.png", width=150)