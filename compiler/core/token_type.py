from enum import Enum

class TokenType(Enum):
    """Tipos de tokens aceitos pelo analisador léxico."""
    
    INTEGER = "INTEGER NUMBER"
    REAL = "REAL NUMBER"
    IDENTIFIER = "IDENTIFIER" # Variáveis, nomes de procedimentos, etc. (começam com letra ou underscore, seguidos de letras, dígitos ou underscores)
    
    
    # OPERADORES ARITMÉTICOS RELACIONAIS E DE ATRIBUIÇÃO
    OP_ADD = "ADDITION"
    OP_SUB = "SUBTRACTION"
    OP_MUL = "MULTIPLICATION"
    OP_DIV = "DIVISION"
    OP_EQ = "EQUALS"
    OP_NEQ = "NOT EQUALS"
    OP_LT = "LESS THAN"
    OP_GT = "GREATER THAN"
    OP_LE = "LESS THAN OR EQUAL TO"
    OP_GE = "GREATER THAN OR EQUAL TO"
    OP_ASSIGN = "ASSIGNMENT"

    #ESPECIAIS
    EOF = "END OF INPUT"
    INVALID = "INVALID TOKEN"

    #DELIMITADORES
    SEMICOLON = "SEMICOLON"
    COLON = "COLON"
    DOT = "DOT"
    LEFT_PAREN = "LEFT PARENTHESIS"
    RIGHT_PAREN = "RIGHT PARENTHESIS"
    COMMA = "COMMA"

    #PALAVRAS-CHAVE (KEYWORDS -> KW)
    KW_PROGRAM = "KEYWORD 'PROGRAM'"
    KW_VAR = "KEYWORD 'VAR'"
    KW_INT = "KEYWORD 'INT'"
    KW_BOOLEAN = "KEYWORD 'BOOLEAN'"
    KW_PROCEDURE = "KEYWORD 'PROCEDURE'"
    KW_BEGIN = "KEYWORD 'BEGIN'"
    KW_END = "KEYWORD 'END'"
    KW_IF = "KEYWORD 'IF'"
    KW_THEN = "KEYWORD 'THEN'"
    KW_ELSE = "KEYWORD 'ELSE'"
    KW_WHILE = "KEYWORD 'WHILE'"
    KW_DO = "KEYWORD 'DO'"
    KW_FOR = "KEYWORD 'FOR'"
    KW_TO = "KEYWORD 'TO'"
    KW_NOT = "KEYWORD 'NOT'"
    KW_OR = "KEYWORD 'OR'"
    KW_AND = "KEYWORD 'AND'"
    KW_READ = "KEYWORD 'READ'"
    KW_WRITE = "KEYWORD 'WRITE'"
    KW_TRUE = "KEYWORD 'TRUE'"
    KW_FALSE = "KEYWORD 'FALSE'"
    KW_RETURN = "KEYWORD 'RETURN'"