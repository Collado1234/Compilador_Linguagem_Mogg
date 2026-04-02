from compiler.core.errors import ParserError
from compiler.core.token import Token
from compiler.core.token_type import TokenType


class Parser:
    """Analisador sintático de descida recursiva para a linguagem LALG."""

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0
        self.errors: list[str] = []
    
    # ── Propriedades e métodos auxiliares ──────────────────────────

    @property
    def _current_token(self) -> Token:
        """Retorna o token atual."""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return self.tokens[-1]  # EOF

    def _advance(self) -> Token:
        """Avança para o próximo token e retorna o token anterior."""
        token = self._current_token
        if self.position < len(self.tokens) - 1:
            self.position += 1
        return token

    def _match(self, *token_types: TokenType) -> bool:
        """Verifica se o token atual é de um dos tipos esperados (sem consumir)."""
        return self._current_token.type in token_types

    def _expect(self, token_type: TokenType) -> Token:
        """Consome o token atual se for do tipo esperado, senão registra erro."""
        if self._current_token.type == token_type:
            return self._advance()
        else:
            token = self._current_token
            self._error(f"Esperado '{token_type.value}', encontrado '{token.value}'")
            return token

    def _error(self, message: str):
        """Registra um erro sintático com linha e coluna."""
        token = self._current_token
        error_msg = f"Erro na linha {token.line}, coluna {token.column}: {message}"
        self.errors.append(error_msg)

    def _sync(self, *sync_types: TokenType):
        """Modo pânico: avança até encontrar um token de sincronização."""
        while not self._match(TokenType.EOF, *sync_types):
            self._advance()

    # ── Ponto de entrada ──────────────────────────────────────────

    def parse(self) -> list[str]:
        """Executa a análise sintática e retorna lista de erros (vazia = sucesso)."""
        self._program()
        if not self.errors:
            self.errors.append("Análise sintática concluída com sucesso!")
        return self.errors

    # ── Regras gramaticais ────────────────────────────────────────

    def _program(self):
        """programa → 'program' identificador ';' bloco '.'"""
        self._expect(TokenType.KW_PROGRAM)
        self._expect(TokenType.IDENTIFIER)
        self._expect(TokenType.SEMICOLON)
        self._block()
        self._expect(TokenType.DOT)

    def _block(self):
        """bloco → [declaração_de_variáveis] {declaração_de_procedimentos} comando_composto"""
        # Declaração de variáveis (opcional)
        if self._match(TokenType.KW_VAR):
            self._variable_declaration_part()

        # Declarações de procedimentos (zero ou mais)
        while self._match(TokenType.KW_PROCEDURE):
            self._procedure_declaration()

        # Comando composto obrigatório
        self._compound_statement()

    # ── Declarações ───────────────────────────────────────────────

    def _variable_declaration_part(self):
        """parte_de_declaração_de_variáveis → 'var' declaração_de_variáveis ';' {declaração_de_variáveis ';'}"""
        self._expect(TokenType.KW_VAR)
        self._variable_declaration()
        self._expect(TokenType.SEMICOLON)

        # Pode ter mais declarações (começa com identificador que é um tipo ou nome de variável)
        while self._match(TokenType.IDENTIFIER, TokenType.KW_INT, TokenType.KW_BOOLEAN):
            self._variable_declaration()
            self._expect(TokenType.SEMICOLON)

    def _variable_declaration(self):
        """declaração_de_variáveis → lista_de_identificadores ':' tipo"""
        self._identifier_list()
        self._expect(TokenType.COLON)
        self._type()

    def _identifier_list(self):
        """lista_de_identificadores → identificador {',' identificador}"""
        self._expect(TokenType.IDENTIFIER)
        while self._match(TokenType.COMMA):
            self._advance()  # consome ','
            self._expect(TokenType.IDENTIFIER)

    def _type(self):
        """tipo → 'int' | 'boolean'"""
        if self._match(TokenType.KW_INT):
            self._advance()
        elif self._match(TokenType.KW_BOOLEAN):
            self._advance()
        else:
            self._error(f"Esperado tipo ('int' ou 'boolean'), encontrado '{self._current_token.value}'")

    def _procedure_declaration(self):
        """declaração_de_procedimento → 'procedure' identificador [parâmetros_formais] ';' bloco ';'"""
        self._expect(TokenType.KW_PROCEDURE)
        self._expect(TokenType.IDENTIFIER)

        # Parâmetros formais (opcional)
        if self._match(TokenType.LEFT_PAREN):
            self._formal_parameters()

        self._expect(TokenType.SEMICOLON)
        self._block()
        self._expect(TokenType.SEMICOLON)

    def _formal_parameters(self):
        """parâmetros_formais → '(' seção_de_parâmetros {';' seção_de_parâmetros} ')'"""
        self._expect(TokenType.LEFT_PAREN)
        self._parameter_section()

        while self._match(TokenType.SEMICOLON):
            self._advance()  # consome ';'
            self._parameter_section()

        self._expect(TokenType.RIGHT_PAREN)

    def _parameter_section(self):
        """seção_de_parâmetros → lista_de_identificadores ':' tipo"""
        self._identifier_list()
        self._expect(TokenType.COLON)
        self._type()

    # ── Comandos ──────────────────────────────────────────────────

    def _compound_statement(self):
        """comando_composto → 'begin' comando {';' comando} 'end'"""
        self._expect(TokenType.KW_BEGIN)

        self._statement()

        while self._match(TokenType.SEMICOLON):
            self._advance()  # consome ';'
            # Evita erro se vier 'end' logo após ';'
            if self._match(TokenType.KW_END):
                break
            self._statement()

        self._expect(TokenType.KW_END)

    def _statement(self):
        """comando → atribuição | chamada_procedimento | comando_composto | 
                     comando_if | comando_while | comando_for | 
                     comando_read | comando_write | (vazio)"""
        token = self._current_token

        if token.type == TokenType.IDENTIFIER:
            # Pode ser atribuição (id := expr) ou chamada de procedimento (id(args))
            self._advance()  # consome o identificador
            if self._match(TokenType.OP_ASSIGN):
                self._assignment_rest()
            elif self._match(TokenType.LEFT_PAREN):
                self._procedure_call_rest()
            # Se não for nem := nem (, é chamada de procedimento sem parâmetros (válido)

        elif token.type == TokenType.KW_BEGIN:
            self._compound_statement()

        elif token.type == TokenType.KW_IF:
            self._if_statement()

        elif token.type == TokenType.KW_WHILE:
            self._while_statement()

        elif token.type == TokenType.KW_FOR:
            self._for_statement()

        elif token.type == TokenType.KW_READ:
            self._read_statement()

        elif token.type == TokenType.KW_WRITE:
            self._write_statement()

        # else: comando vazio (permitido pela gramática)

    def _assignment_rest(self):
        """resto_da_atribuição → ':=' expressão (identificador já consumido)"""
        self._expect(TokenType.OP_ASSIGN)
        self._expression()

    def _procedure_call_rest(self):
        """resto_da_chamada → '(' lista_expressões ')' (identificador já consumido)"""
        self._expect(TokenType.LEFT_PAREN)
        self._expression_list()
        self._expect(TokenType.RIGHT_PAREN)

    def _expression_list(self):
        """lista_de_expressões → expressão {',' expressão}"""
        self._expression()
        while self._match(TokenType.COMMA):
            self._advance()  # consome ','
            self._expression()

    def _if_statement(self):
        """comando_if → 'if' expressão 'then' comando ['else' comando]"""
        self._expect(TokenType.KW_IF)
        self._expression()
        self._expect(TokenType.KW_THEN)
        self._statement()

        if self._match(TokenType.KW_ELSE):
            self._advance()  # consome 'else'
            self._statement()

    def _while_statement(self):
        """comando_while → 'while' expressão 'do' comando"""
        self._expect(TokenType.KW_WHILE)
        self._expression()
        self._expect(TokenType.KW_DO)
        self._statement()

    def _for_statement(self):
        """comando_for → 'for' identificador ':=' expressão 'to' expressão 'do' comando"""
        self._expect(TokenType.KW_FOR)
        self._expect(TokenType.IDENTIFIER)
        self._expect(TokenType.OP_ASSIGN)
        self._expression()
        self._expect(TokenType.KW_TO)
        self._expression()
        self._expect(TokenType.KW_DO)
        self._statement()

    def _read_statement(self):
        """comando_read → 'read' '(' lista_de_identificadores ')'"""
        self._expect(TokenType.KW_READ)
        self._expect(TokenType.LEFT_PAREN)
        self._identifier_list()
        self._expect(TokenType.RIGHT_PAREN)

    def _write_statement(self):
        """comando_write → 'write' '(' lista_de_expressões ')'"""
        self._expect(TokenType.KW_WRITE)
        self._expect(TokenType.LEFT_PAREN)
        self._expression_list()
        self._expect(TokenType.RIGHT_PAREN)

    # ── Expressões ────────────────────────────────────────────────

    def _expression(self):
        """expressão → expressão_simples [operador_relacional expressão_simples]"""
        self._simple_expression()

        if self._match(TokenType.OP_EQ, TokenType.OP_NEQ, TokenType.OP_LT,
                       TokenType.OP_GT, TokenType.OP_LE, TokenType.OP_GE):
            self._advance()  # consome o operador relacional
            self._simple_expression()

    def _simple_expression(self):
        """expressão_simples → ['+' | '-'] termo {('+' | '-' | 'or') termo}"""
        # Sinal opcional no início
        if self._match(TokenType.OP_ADD, TokenType.OP_SUB):
            self._advance()

        self._term()

        while self._match(TokenType.OP_ADD, TokenType.OP_SUB, TokenType.KW_OR):
            self._advance()  # consome o operador
            self._term()

    def _term(self):
        """termo → fator {('*' | '/' | 'and') fator}"""
        self._factor()

        while self._match(TokenType.OP_MUL, TokenType.OP_DIV, TokenType.KW_AND):
            self._advance()  # consome o operador
            self._factor()

    def _factor(self):
        """fator → identificador [chamada] | número | '(' expressão ')' | 'not' fator | 'true' | 'false'"""
        token = self._current_token

        if token.type == TokenType.IDENTIFIER:
            self._advance()
            # Pode ser chamada de função: identificador '(' lista_expressões ')'
            if self._match(TokenType.LEFT_PAREN):
                self._expect(TokenType.LEFT_PAREN)
                self._expression_list()
                self._expect(TokenType.RIGHT_PAREN)

        elif token.type in (TokenType.INTEGER, TokenType.REAL):
            self._advance()

        elif token.type == TokenType.LEFT_PAREN:
            self._advance()  # consome '('
            self._expression()
            self._expect(TokenType.RIGHT_PAREN)

        elif token.type == TokenType.KW_NOT:
            self._advance()  # consome 'not'
            self._factor()

        elif token.type in (TokenType.KW_TRUE, TokenType.KW_FALSE):
            self._advance()

        else:
            self._error(f"Fator esperado, encontrado '{token.value}'")
            self._advance()  # avança para evitar loop infinito