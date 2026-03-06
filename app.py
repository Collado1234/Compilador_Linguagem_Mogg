from io import StringIO
import streamlit as st
import pandas as pd

from compiler.errors import LexerError
from compiler.lexer import Lexer
from compiler.parser import Parser

st.markdown("<h1 style='text-align: center;'>Compilador</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Analisador Léxico", "Analisador Sintático"])

with tab1:
    if 'df' not in st.session_state:
        st.session_state['df'] = pd.DataFrame()

    if 'text_area' not in st.session_state:
        st.session_state['text_area'] = None

    st.markdown("<h2 style='text-align: center;'>Analisador Léxico</h2>", unsafe_allow_html=True)

    file_uploader = st.file_uploader(key="file_uploader", label="Carregar expressão matemática", type=['txt'], max_upload_size=1, accept_multiple_files=False, width="stretch")

    if file_uploader:
        stringio = StringIO(file_uploader.getvalue().decode("utf-8"))
        st.session_state['text_area'] = stringio.read()

    sample = "(10 + 5.5) / 2 - 0.25"

    if st.session_state['text_area'] is None:
        st.session_state['text_area'] = sample

    text_area = st.text_area("Expressão matemática:", value=st.session_state['text_area'], height="content")

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

    with col3:
        run_button = st.button("Analisar", key=1, icon=":material/check:")

    # Tokens válidos para expressões matemáticas
    TOKENS_VALIDOS_EXPRESSAO = {
        "INTEGER", "REAL", "OP_ADD", "OP_SUB", "OP_MUL", "OP_DIV",
        "LEFT_PAREN", "RIGHT_PAREN", "EOF"
    }
    
    OPERADORES = {"OP_ADD", "OP_SUB", "OP_MUL", "OP_DIV"}
    OPERANDOS = {"INTEGER", "REAL"}

    if run_button:
        try:
            lexer = Lexer(text_area)
            tokens, erros = lexer.generate_tokens()

            # Validar tokens para expressões matemáticas
            for token in tokens:
                if token.type.name not in TOKENS_VALIDOS_EXPRESSAO:
                    erros.append({
                        "tipo": "Token inválido para expressão",
                        "linha": token.line,
                        "coluna": token.column,
                        "mensagem": f"'{token.value}' não é válido em expressões matemáticas"
                    })
                    lexer.has_errors = True

            # Validação sintática simples
            tokens_sem_eof = [t for t in tokens if t.type.name != "EOF"]
            for i, token in enumerate(tokens_sem_eof):
                tipo_atual = token.type.name
                
                # Verifica operadores consecutivos (exceto - unário após outro operador)
                if i > 0:
                    tipo_anterior = tokens_sem_eof[i-1].type.name
                    
                    # Dois operadores consecutivos (exceto - após operador para negativo)
                    if tipo_atual in OPERADORES and tipo_anterior in OPERADORES:
                        if not (tipo_atual == "OP_SUB" and tipo_anterior in OPERADORES):
                            erros.append({
                                "tipo": "Erro sintático",
                                "linha": token.line,
                                "coluna": token.column,
                                "mensagem": f"Operadores consecutivos: '{tokens_sem_eof[i-1].value}' seguido de '{token.value}'"
                            })
                            lexer.has_errors = True
                    
                    # Dois operandos consecutivos sem operador
                    if tipo_atual in OPERANDOS and tipo_anterior in OPERANDOS:
                        erros.append({
                            "tipo": "Erro sintático",
                            "linha": token.line,
                            "coluna": token.column,
                            "mensagem": f"Falta operador entre '{tokens_sem_eof[i-1].value}' e '{token.value}'"
                        })
                        lexer.has_errors = True
                
                # Expressão começa com operador binário (* ou /)
                if i == 0 and tipo_atual in {"OP_MUL", "OP_DIV"}:
                    erros.append({
                        "tipo": "Erro sintático",
                        "linha": token.line,
                        "coluna": token.column,
                        "mensagem": f"Expressão não pode começar com '{token.value}'"
                    })
                    lexer.has_errors = True
            
            # Expressão termina com operador
            if tokens_sem_eof and tokens_sem_eof[-1].type.name in OPERADORES:
                ultimo = tokens_sem_eof[-1]
                erros.append({
                    "tipo": "Erro sintático",
                    "linha": ultimo.line,
                    "coluna": ultimo.column,
                    "mensagem": f"Expressão não pode terminar com '{ultimo.value}'"
                })
                lexer.has_errors = True

            if erros:
                st.error("Erros encontrados:")
                st.dataframe(pd.DataFrame(erros))

            df = pd.DataFrame(
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
            st.session_state['df'] = df
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
    sample2 = """program exemplo;
var x, y: int;
begin
x := 10;
y := 20;
write(x + y)
end."""

    if 'df2' not in st.session_state:
        st.session_state['df2'] = pd.DataFrame()

    if 'text_area2' not in st.session_state:
        st.session_state['text_area2'] = None

    st.markdown("<h2 style='text-align: center;'>Analisador Sintático</h2>", unsafe_allow_html=True)

    file_uploader2 = st.file_uploader(key="file_uploader2", label="Carregar código", type=['txt'], max_upload_size=1, accept_multiple_files=False, width="stretch")

    if file_uploader2:
        stringio2 = StringIO(file_uploader2.getvalue().decode("utf-8"))
        st.session_state['text_area2'] = stringio2.read()

    if st.session_state['text_area2'] is None:
        st.session_state['text_area2'] = sample2
    
    text_area2 = st.text_area("Código LALG:", value=st.session_state['text_area2'], height="content", key="text_area2")

    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

    with col3:
        run_button2 = st.button("Analisar", key=3, icon=":material/check:")

    if run_button2:
        try:
            # Análise Léxica
            lexer = Lexer(text_area2)
            tokens, erros_lexicos = lexer.generate_tokens()

            # Mostrar tokens
            df_pandas2 = pd.DataFrame(
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
            st.session_state['df2'] = df_pandas2

            if erros_lexicos:
                st.error("Erros léxicos encontrados:")
                st.dataframe(pd.DataFrame(erros_lexicos))
                st.session_state['has_errors2'] = True
                st.session_state['parser_errors'] = []
            else:
                # Análise Sintática (só roda se não houver erros léxicos)
                parser = Parser(tokens)
                erros_sintaticos = parser.parse()
                st.session_state['parser_errors'] = erros_sintaticos
                st.session_state['has_errors2'] = len(erros_sintaticos) > 1 or "sucesso" not in erros_sintaticos[0].lower()

        except LexerError as error:
            st.error(str(error))

    if 'df2' in st.session_state and st.session_state['df2'].empty == False:
        # Mostrar resultado da análise sintática
        if 'parser_errors' in st.session_state:
            for msg in st.session_state['parser_errors']:
                if "sucesso" in msg.lower():
                    st.success(msg)
                else:
                    st.error(msg)
        
        st.subheader("Tokens encontrados:")
        st.dataframe(st.session_state['df2'])

        csv2 = st.session_state['df2'].to_csv(index=False).encode("utf-8")
        st.download_button(label="Baixar CSV", data=csv2, file_name="data_sintatico.csv", icon=":material/download:", disabled=False, key="download2")