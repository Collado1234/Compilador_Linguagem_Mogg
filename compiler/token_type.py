from enum import Enum

class TokenType(Enum):
    """Tipos de tokens aceitos pelo analisador léxico."""
    
    INTEGER = "INTEGER NUMBER"
    REAL = "REAL NUMBER"
    LEFT_PAREN = "LEFT PARENTHESIS"
    RIGHT_PAREN = "RIGHT PARENTHESIS"
    OP_ADD = "ADDITION"
    OP_SUB = "SUBTRACTION"
    OP_MUL = "MULTIPLICATION"
    OP_DIV = "DIVISION"
    EOF = "END OF INPUT"