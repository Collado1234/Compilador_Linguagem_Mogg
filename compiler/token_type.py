from enum import Enum

class TokenType(Enum):
    iNum = "INTEGER NUMBER"
    rNum = "REAL NUMBER"
    lParen = "LEFT PARENTHESIS"
    rParen = "RIGHT PARENTHESIS"
    opAdd = "ADDITION"
    opSub = "SUBTRACTION"
    opMul = "MULTIPLICATION"
    opDiv = "DIVISION"