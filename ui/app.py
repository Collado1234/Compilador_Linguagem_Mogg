"""
app.py

Interface gráfica do compilador utilizando Streamlit.

Responsabilidades:
- Receber entrada do usuário (texto ou arquivo)
- Acionar os serviços de análise léxica e sintática
- Exibir tokens e erros de forma visual (tabelas)
- Permitir exportação dos resultados em CSV

IMPORTANTE:
Este módulo NÃO contém lógica de compilador.
Toda a lógica está encapsulada em:
- services.lexical_services
- compiler.parser

Arquitetura:
UI (Streamlit) → Services → Core (Lexer/Parser)
"""

from io import StringIO
import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from compiler.core.errors import LexerError
from services.lexical_services import analyze_lexical
from compiler.parser import Parser


# =========================
# Helpers (APENAS UI)
# =========================

def tokens_to_dataframe(tokens):
    """
    Converte uma lista de tokens em um DataFrame do pandas.

    Parâmetros:
        tokens (list[Token]): Lista de tokens gerados pelo lexer.

    Retorno:
        pandas.DataFrame: Estrutura tabular para exibição no Streamlit.
    """
    return pd.DataFrame([
        {
            "Token": t.type.name,
            "Descrição": t.type.value,
            "Lexema": t.value,
            "Linha": t.line,
            "Coluna Inicial": t.column,
            "Coluna Final": t.end_column,
        }
        for t in tokens
    ])


def load_file(file):
    """
    Lê o conteúdo de um arquivo carregado pelo Streamlit.

    Parâmetros:
        file: Arquivo recebido pelo st.file_uploader

    Retorno:
        str: Conteúdo do arquivo em formato texto
    """
    return StringIO(file.getvalue().decode("utf-8")).read()


# =========================
# UI PRINCIPAL
# =========================

st.markdown("<h1 style='text-align: center;'>Compilador</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Analisador Léxico", "Analisador Sintático"])


# =========================
# TAB 1 - ANÁLISE LÉXICA
# =========================

with tab1:
    st.markdown("<h2 style='text-align: center;'>Analisador Léxico</h2>", unsafe_allow_html=True)

    # Inicialização do estado
    if 'df' not in st.session_state:
        st.session_state['df'] = pd.DataFrame()

    if 'text_area' not in st.session_state:
        st.session_state['text_area'] = """program exemplo;
var x, y: int;
begin
x := 10;
y := 20;
write(x + y)
end."""

    # Upload de arquivo
    file = st.file_uploader("Carregar código LALG", type=['txt'])

    if file:
        st.session_state['text_area'] = load_file(file)

    # Entrada manual
    text = st.text_area("Código LALG:", value=st.session_state['text_area'])

    # Botão centralizado
    _, _, col, _, _ = st.columns(5)
    run = col.button("Analisar", icon=":material/check:")

    # Execução da análise léxica
    if run:
        try:
            result = analyze_lexical(text)

            tokens = result["tokens"]
            errors = result["errors"]

            # Exibição de erros léxicos
            if errors:
                st.error("Erros encontrados:")
                st.dataframe(pd.DataFrame(errors))

            # Conversão para tabela
            df = tokens_to_dataframe(tokens)

            st.session_state['df'] = df
            st.session_state['has_errors'] = result["has_errors"]

        except LexerError as e:
            st.error(str(e))

    # Exibição dos resultados
    if not st.session_state['df'].empty:
        if st.session_state.get('has_errors'):
            st.warning("A análise léxica foi concluída com erros.")
        else:
            st.success("Análise léxica concluída com sucesso.")

        st.dataframe(st.session_state['df'])

        # Download CSV
        st.download_button(
            label="Baixar CSV",
            data=st.session_state['df'].to_csv(index=False).encode("utf-8"),
            file_name="lexico.csv"
        )


# =========================
# TAB 2 - ANÁLISE SINTÁTICA
# =========================

with tab2:
    st.markdown("<h2 style='text-align: center;'>Analisador Sintático</h2>", unsafe_allow_html=True)

    # Código exemplo
    sample = """program exemplo;
var x, y: int;
begin
x := 10;
y := 20;
write(x + y)
end."""

    # Inicialização do estado
    if 'df2' not in st.session_state:
        st.session_state['df2'] = pd.DataFrame()

    if 'text_area2' not in st.session_state:
        st.session_state['text_area2'] = sample

    # Upload de arquivo
    file = st.file_uploader("Carregar código", type=['txt'], key="file2")

    if file:
        st.session_state['text_area2'] = load_file(file)

    # Entrada manual
    text = st.text_area("Código LALG:", value=st.session_state['text_area2'])

    # Botão de execução
    _, _, col, _, _ = st.columns(5)
    run = col.button("Analisar", key=2, icon=":material/check:")

    if run:
        try:
            # Etapa 1: análise léxica
            result = analyze_lexical(text)

            tokens = result["tokens"]
            errors = result["errors"]

            # Exibir tokens
            df = tokens_to_dataframe(tokens)
            st.session_state['df2'] = df

            # Se houver erro léxico, não roda parser
            if errors:
                st.error("Erros léxicos encontrados:")
                st.dataframe(pd.DataFrame(errors))
                st.session_state['parser_errors'] = []
            else:
                # Etapa 2: análise sintática
                parser = Parser(tokens)
                st.session_state['parser_errors'] = parser.parse()

        except LexerError as e:
            st.error(str(e))

    # Exibição dos resultados
    if not st.session_state['df2'].empty:

        # Mensagens do parser
        if 'parser_errors' in st.session_state:
            for msg in st.session_state['parser_errors']:
                if "sucesso" in msg.lower():
                    st.success(msg)
                else:
                    st.error(msg)

        st.subheader("Tokens encontrados:")
        st.dataframe(st.session_state['df2'])

        # Download CSV
        st.download_button(
            label="Baixar CSV",
            data=st.session_state['df2'].to_csv(index=False).encode("utf-8"),
            file_name="sintatico.csv"
        )