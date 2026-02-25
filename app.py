import streamlit as st

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    title = st.text_area("Expressão matemática:", width=300, height=400)
with col2:
    lexema = st.write("Lexema")
with col3:
    token = st.write("Token")

run_button = st.button("Compilar", icon=":material/check:", width="stretch")