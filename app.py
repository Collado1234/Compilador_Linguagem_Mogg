import streamlit as st

from compiler.errors import LexerError
from compiler.lexer import Lexer

st.markdown("<h1 style='text-align: center;'>Compilador - Analisador Léxico</h1>", unsafe_allow_html=True)

sample = "(10 + 5.5) / 2 - .25"
text_area = st.text_area("Expressão matemática:", value=sample, height=180)

col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

with col3:
    run_button = st.button("Analisar", icon=":material/check:")

if run_button:
    try:
        lexer = Lexer(text_area)
        tokens = lexer.generate_tokens()

        st.success("Análise léxica concluída com sucesso.")
        st.dataframe(
            [
                {
                    "Token": token.type.name,
                    "Descrição": token.type.value,
                    "Lexema": token.value,
                    "Linha": token.line,
                    "Coluna": token.column,
                }
                for token in tokens
            ],
            width="stretch",
        )
    except LexerError as error:
        st.error(str(error))