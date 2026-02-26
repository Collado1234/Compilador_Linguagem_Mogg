import streamlit as st
import pandas as pd

from compiler.errors import LexerError
from compiler.lexer import Lexer

st.markdown("<h1 style='text-align: center;'>Compilador - Analisador Léxico</h1>", unsafe_allow_html=True)

file_uploader = st.file_uploader(label="Carregar expressão matemática", max_upload_size=1, accept_multiple_files=False, width="stretch")

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
        df_streamlit = st.dataframe(
            [
                {
                    "Token": token.type.name,
                    "Descrição": token.type.value,
                    "Lexema": token.value,
                    "Linha": token.line,
                    "Coluna": token.column,
                }
                for token in tokens
            ]
        )

        df_pandas = pd.DataFrame(
            [
                {
                    "Token": token.type.name,
                    "Descrição": token.type.value,
                    "Lexema": token.value,
                    "Linha": token.line,
                    "Coluna": token.column,
                }
                for token in tokens
            ]
        )

        csv = df_pandas.to_csv(index=False).encode("utf-8")

        download_button = st.download_button(label="Baixar CSV", data=csv, file_name="data.csv", icon=":material/download:")
    except LexerError as error:
        st.error(str(error))