from compiler.core.errors import ScannerError
from compiler.core.token import Token
from compiler.core.token_type import TokenType

class Scanner:
    "Analisador léxico para a lingaugem LALG"

    RESERVED_WORDS = {
        "program": TokenType.KW_PROGRAM,
        "var": TokenType.KW_VAR,
        "int": TokenType.KW_INT,
        "boolean": TokenType.KW_BOOLEAN,
        "procedure": TokenType.KW_PROCEDURE,
        "begin": TokenType.KW_BEGIN,
        "end": TokenType.KW_END,
        "if": TokenType.KW_IF,
        "then": TokenType.KW_THEN,
        "else": TokenType.KW_ELSE,
        "while": TokenType.KW_WHILE,
        "do": TokenType.KW_DO,
        "for": TokenType.KW_FOR,
        "to": TokenType.KW_TO,
        "not": TokenType.KW_NOT,
        "or": TokenType.KW_OR,
        "and": TokenType.KW_AND,
        "read": TokenType.KW_READ,
        "write": TokenType.KW_WRITE,
        "true": TokenType.KW_TRUE,
        "false": TokenType.KW_FALSE,
        "return": TokenType.KW_RETURN,
    }

    SINGLE_CHAR_TOKENS = {
        "+": TokenType.OP_ADD,
        "-": TokenType.OP_SUB,
        "*": TokenType.OP_MUL,
        "(": TokenType.LEFT_PAREN,
        ")": TokenType.RIGHT_PAREN,
        ";": TokenType.SEMICOLON,
        ",": TokenType.COMMA,
        "=": TokenType.OP_EQ,
    }

    def __init__(self, text: str):
        self.text = text or ""
        self.position = 0
        self.line = 1
        self.column = 1
        self.has_errors = False
        self.errors = []  # Lista para registrar erros
    
    def generate_tokens(self):
        tokens: list[Token] = []
        

        while self._current_char is not None:
            current_char = self._current_char

            if current_char.isspace():
                self._advance()
                continue

            if current_char == "{": #Bloco de comentário
                self._skip_block_comment()
                continue

            if current_char.isalpha() or current_char == "_": #Identificadores e palavras-chave
                tokens.append(self._generate_identifier_or_keyword())
                continue

            if current_char.isdigit(): #Não permite mais que comece com .
                tokens.append(self._generate_number())
                continue

            if current_char == "/": #Pode ser comentário de linha ou operador de divisão
                if self._peek() == "/":
                    self._skip_line_comment()
                    continue
                else:
                    tokens.append(Token(TokenType.OP_DIV, current_char, self.line, self.column, self.column))
                    self._advance()
                    continue
            
            if current_char == ":": #Pode ser operador de atribuição ou delimitador de declaração
                start_col = self.column
                if self._peek() == "=":
                    self._advance() # Avança sobre o :
                    self._advance() # Avança sobre o =
                    tokens.append(Token(TokenType.OP_ASSIGN, ":=", self.line, start_col, self.column - 1)) 
                else:
                    tokens.append(Token(TokenType.COLON, current_char, self.line, start_col, start_col))
                    self._advance()
                continue

            if current_char == "<": #Pode ser <, <= ou <>
                start_col = self.column
                next_char = self._peek()
                if next_char == ">":
                    self._advance() # Avança sobre o <
                    self._advance() # Avança sobre o >
                    tokens.append(Token(TokenType.OP_NEQ, "<>", self.line, start_col, self.column - 1))
                elif next_char == "=":
                    self._advance() # Avança sobre o <
                    self._advance() # Avança sobre o =
                    tokens.append(Token(TokenType.OP_LE, "<=", self.line, start_col, self.column - 1))
                else:
                    tokens.append(Token(TokenType.OP_LT, "<", self.line, start_col, start_col))
                    self._advance()
                continue

            if current_char == ">": #Pode ser > ou >=
                start_col = self.column
                if self._peek() == "=":
                    self._advance() # Avança sobre o >
                    self._advance() # Avança sobre o =
                    tokens.append(Token(TokenType.OP_GE, ">=", self.line, start_col, self.column - 1))
                else:
                    tokens.append(Token(TokenType.OP_GT, current_char, self.line, start_col, start_col))
                    self._advance()
                continue

            if current_char == ".":
                tokens.append(Token(TokenType.DOT, ".", self.line, self.column, self.column))
                self._advance()
                continue

            token_type = self.SINGLE_CHAR_TOKENS.get(current_char) 
            if token_type is not None:
                token = Token(token_type, current_char, self.line, self.column, self.column) # O token de operador tem início e fim na mesma coluna
                tokens.append(token)
                self._advance()
                continue

            #Como queremos que ele n pare vamos criar um token mesmo assim, mas marcando como inválido
            self.has_errors = True
            self.errors.append({
                "tipo": "Caractere inválido",
                "linha": self.line,
                "coluna": self.column,
                "mensagem": f"Caractere '{current_char}' não reconhecido"
            })
            token = Token(TokenType.INVALID, current_char, self.line, self.column, self.column)
            tokens.append(token)
            self._advance()

        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens, self.errors  # Retorna tokens e lista de erros

    @property
    def _current_char(self) -> str | None:
        if self.position >= len(self.text):
            return None
        return self.text[self.position]
    
    def _peek(self) -> str | None:
        peek_pos = self.position + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]

    def _advance(self) -> None:
        if self._current_char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.position += 1

    def _generate_identifier_or_keyword(self) -> Token: #Ler um identificador ou palavra-chave
        start_line = self.line
        start_column = self.column
        char = []

        while self._current_char is not None and (self._current_char.isalnum() or self._current_char == "_"):
            char.append(self._current_char)
            self._advance()

        lexeme = "".join(char)
        end_column = self.column - 1 # O token termina na coluna anterior à posição atual
        # Consulta a tabela de palavras reservadas (case-insensitive)
        token_type = self.RESERVED_WORDS.get(lexeme.lower(), TokenType.IDENTIFIER)

        return Token(token_type, lexeme, start_line, start_column, end_column)


    def _generate_number(self) -> Token:
        """Lê um número inteiro ou real (não começa com ponto)."""
        start_line = self.line
        start_column = self.column
        number = []
        has_decimal_point = False

        while self._current_char is not None:
            if self._current_char.isdigit():
                number.append(self._current_char)
                self._advance()
            elif self._current_char == "." and not has_decimal_point:
                # Só aceita ponto se o próximo char for dígito (senão é DOT)
                if self._peek() is not None and self._peek().isdigit():
                    has_decimal_point = True
                    number.append(self._current_char)
                    self._advance()
                else:
                    break  # O ponto será tratado como DOT
            else:
                break

        lexeme = "".join(number)
        token_type = TokenType.REAL if has_decimal_point else TokenType.INTEGER
        end_column = self.column - 1

        return Token(token_type, lexeme, start_line, start_column, end_column)
    
    def _skip_block_comment(self) -> None: #Pula comentario de bloco e da erro se n fechar
        start_line = self.line
        start_column = self.column
        self._advance() # Avança sobre o {

        while self._current_char is not None:
            if self._current_char == "}":
                self._advance() # Avança sobre o }
                return
            self._advance()

        # Registra o erro sem levantar exceção
        self.has_errors = True
        self.errors.append({
            "tipo": "Comentário não fechado",
            "linha": start_line,
            "coluna": start_column,
            "mensagem": "Comentário de bloco não fechado"
        })
        # Remove o raise LexerError(...)

    def _skip_line_comment(self) -> None: #Pula comentário de linha
        while self._current_char is not None and self._current_char != "\n":
            self._advance()