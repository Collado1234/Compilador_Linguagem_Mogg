from compiler.core.token import Token
from compiler.core.token_type import TokenType

class Symbol_Table:
    def __init__(self):
        self.tokens = {}
        size = 0

    def add(self, token: Token):
        lexeme = token.value
        
        if lexeme in self.tokens:
             raise Exception (f"Variável {lexeme} já declarada.")
        
        self.tokens[lexeme] = token
        
    def get(self, lexeme: str):
        self.tokens.get(lexeme)

    def exists(self, lexeme: str):
        return lexeme in self.tokens