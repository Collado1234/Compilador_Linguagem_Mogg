from compiler.analysis.scanner import Scanner

def analyze_lexical(text: str):
    lexer = Scanner(text)
    tokens, errors = lexer.generate_tokens()

    return {
        "tokens": tokens,
        "errors": errors,
        "has_errors": lexer.has_errors
    }