from io import StringIO
import streamlit as st
import pandas as pd

from compiler.errors import LexerError
from compiler.lexer import Lexer

st.markdown("<h1 style='text-align: center;'>Compilador</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Analisador Léxico", "Analisador Sintático"])

with tab1:
    if 'df' not in st.session_state:
        st.session_state['df'] = pd.DataFrame()

    if 'upload' not in st.session_state:
        st.session_state['upload'] = None

    st.markdown("<h2 style='text-align: center;'>Analisador Léxico</h2>", unsafe_allow_html=True)

    file_uploader = st.file_uploader(key=0, label="Carregar expressão matemática", type=['txt'], max_upload_size=1, accept_multiple_files=False, width="stretch")
    file_text = None

    if file_uploader:
        st.session_state['upload'] = file_uploader
        stringio = StringIO(file_uploader.getvalue().decode("utf-8"))
        file_text = stringio.read()

    sample = "(10 + 5.5) / 2 - .25"

    if st.session_state['upload'] is None:
        text_area = st.text_area("Expressão matemática:", value=sample, height=180)
    else:
        text_area = st.text_area("Expressão matemática:", value=file_text, height=180)

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

    with col3:
        run_button = st.button("Analisar", key=1, icon=":material/check:")

    if run_button:
        try:
            lexer = Lexer(text_area)
            tokens = lexer.generate_tokens()

            df_pandas = pd.DataFrame(
                [
                    {
                        "Token": token.type.name,
                        "Descrição": token.type.value,
                        "Lexema": token.value,
                        "Linha": token.line,
                        "Coluna Inicial": token.column,
                        "Coluna Final": token.end_column,
                    }
                    for token in tokens 
                ]
            )
            st.session_state['df'] = df_pandas
            st.session_state['has_errors'] = lexer.has_errors # Podemos usar isso para mostrar uma mensagem de aviso se houver erros léxicos, mas ainda assim mostrar os tokens encontrados.
        except LexerError as error:
            st.error(str(error))

    if st.session_state['df'].empty == False:
        if st.session_state.get('has_errors', False):
            st.warning("A análise léxica foi concluída, mas foram encontrados caracteres inválidos. Verifique os tokens listados para mais detalhes.")
        else:
            st.success("Análise léxica concluída com sucesso.")
        df_streamlit = st.dataframe(
            st.session_state['df']
        )

        csv = st.session_state['df'].to_csv(index=False).encode("utf-8")
        download_button = st.download_button(label="Baixar CSV", data=csv, file_name="data.csv", icon=":material/download:", disabled=False)    

with tab2:
    if 'df' not in st.session_state:
        st.session_state['df'] = pd.DataFrame()

    if 'upload' not in st.session_state:
        st.session_state['upload'] = None

    st.markdown("<h2 style='text-align: center;'>Analisador Sintático</h2>", unsafe_allow_html=True)

    file_uploader = st.file_uploader(key=2, label="Carregar código", type=['txt'], max_upload_size=1, accept_multiple_files=False, width="stretch")
    file_text = None

    if file_uploader:
        st.session_state['upload'] = file_uploader
        stringio = StringIO(file_uploader.getvalue().decode("utf-8"))
        file_text = stringio.read()

    sample = """program ola_mundo;
                    { a LALG aceita tipos int e boolean! }
                    int alfa, beta;
                    boolean omega;
                { você pode declarar e chamar procedimentos! }
                procedure soma(a, b: int);
                begin
                    write(a + b)
                end;
                begin
                    {
                    remova os comentários abaixo para remover o
                    erro semântico de omega
                    }
                    //omega := true;
                    alfa := 1;
                    beta := 2;
                    soma(alfa, beta)
                end.
            """

    if st.session_state['upload'] is None:
        text_area = st.text_area("LALG", value=sample, height="content")
    else:
        text_area = st.text_area("LALG", value=file_text, height="content")

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

    with col3:
        run_button = st.button("Analisar", key=3, icon=":material/check:")