# services/lexical_service.py

from compiler.lexer.lexer import Lexer

def analyze_lexical(text: str):
    lexer = Lexer(text)
    tokens, errors = lexer.generate_tokens()

    return {
        "tokens": tokens,
        "errors": errors,
        "has_errors": lexer.has_errors
    }