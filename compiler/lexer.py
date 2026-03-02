from compiler.errors import LexerError
from compiler.token import Token
from compiler.token_type import TokenType

class Lexer:
    "Analisador semântico para expressões aritméticas"

    SINGLE_CHAR_TOKENS = {
            "+": TokenType.OP_ADD,
        "-": TokenType.OP_SUB,
        "*": TokenType.OP_MUL,
        "/": TokenType.OP_DIV,
        "(": TokenType.LEFT_PAREN,
        ")": TokenType.RIGHT_PAREN,
    }

    def __init__(self, text: str):
        self.text = text or ""
        self.position = 0
        self.line = 1
        self.column = 1
    
    def generate_tokens(self):
        tokens: list[tokens] = []
        self.has_errors = False

        while self._current_char is not None:
            current_char = self._current_char

            if current_char.isspace():
                self._advance()
                continue

            if current_char.isdigit() or current_char == ".": #Permite que um n real comece com ponto ou termine com ponto
                tokens.append(self._generate_number())
                continue

            token_type = self.SINGLE_CHAR_TOKENS.get(current_char) 
            if token_type:
                token = Token(token_type, current_char, self.line, self.column, self.column) # O token de operador tem início e fim na mesma coluna
                tokens.append(token)
                self._advance()
                continue

            #Como queremos que ele n pare vamos criar um token mesmo assim, mas marcando como inválido
            token = Token(TokenType.INVALID, current_char, self.line, self.column, self.column)
            tokens.append(token)
            self.has_errors = True
            self._advance()

            # raise LexerError(f"Caractere inválido: '{current_char}'", self.line, self.column)

        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens

    @property
    def _current_char(self) -> str | None:
        if self.position >= len(self.text):
            return None
        return self.text[self.position]

    def _advance(self) -> None:
        if self._current_char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.position += 1

    def _generate_number(self) -> Token:
        start_line = self.line
        start_column = self.column
        number = []
        has_decimal_point = False
        has_digit = False

        while self._current_char is not None:
            current_char = self._current_char

            if current_char == ".":
                if has_decimal_point:
                    raise LexerError("Número real inválido (múltiplos pontos)", self.line, self.column)
                has_decimal_point = True
                number.append(current_char)
                self._advance()
                continue

            if not current_char.isdigit():
                break

            has_digit = True
            number.append(current_char)
            self._advance()

        lexeme = "".join(number)

        if not has_digit:
            raise LexerError("Numero inválido", start_line, start_column)
        
        if lexeme.startswith("."):
            lexeme = f"0{lexeme}"

        if lexeme.endswith("."):
            lexeme = f"{lexeme}0"
        
        token_type = TokenType.REAL if has_decimal_point else TokenType.INTEGER
        end_column = self.column - 1 # O token termina na coluna anterior à posição atual
        return Token(token_type, lexeme, start_line, start_column, end_column)