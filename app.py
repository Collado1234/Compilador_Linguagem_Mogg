import streamlit as st

from compiler.lexer import Lexer

st.markdown("<h1 style='text-align: center;'>Compilador</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    text_area = st.text_area("Expressão matemática:", width=300, height=400)

run_button = st.button("Compilar", icon=":material/check:")

if run_button:
    lexer = Lexer(text_area)
    tokens = lexer.generate_tokens()
    
    with col2:
        lexema = st.subheader("Lexema")
        for token in tokens:
            st.write(token.value)
    with col3:
        token = st.write("Token")
        for token in tokens:
            st.write(token)