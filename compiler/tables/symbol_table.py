from compiler.core.token import Token
from compiler.core.token_type import TokenType

class Symbol_Table:
    def __init__(self):
        self.tokens = {}
        self.reserved_words = {
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
            "return": TokenType.KW_RETURN
        }

    def add(self, token: Token):
        lexeme = token.value.lower()
        
        self.tokens[lexeme] = token
        
    def get_reserved_words(self, lexeme: str, default=None):
        lexeme = lexeme.lower()
        return self.reserved_words.get(lexeme, self.tokens.get(lexeme, default))

    def exists(self, lexeme: str):
        return lexeme in self.tokens