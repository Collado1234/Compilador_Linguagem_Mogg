from utils import format_error
from compiler.token import Token;
from compiler.token_type import TokenType;

class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = 0

    def generate_tokens(self):
        tokens = []
        while self.position < len(self.text):
            current_char = self.text[self.position]

            if current_char.isdigit():
                tokens.append(self._generate_number())

            elif current_char == '+':
                tokens.append(Token(TokenType.opAdd, '+'))
                self.position += 1

            elif current_char == '-':
                tokens.append(Token(TokenType.opSub, '-'))
                self.position += 1

            elif current_char == '*':
                tokens.append(Token(TokenType.opMul, '*'))
                self.position += 1

            elif current_char == '/':
                tokens.append(Token(TokenType.opDiv, '/'))
                self.position += 1

            elif current_char == '(':
                tokens.append(Token(TokenType.lParen, '('))
                self.position += 1

            elif current_char == ')':
                tokens.append(Token(TokenType.rParen, ')'))
                self.position += 1

            else:
                raise Exception(format_error("Caractere inválido", line, column))
            
    def _generate_number(self):
        number_str = ""
        while self.position < len(self.text) and self.text[self.position].isdigit():
            number_str += self.text[self.position]
            self.position += 1

        return Token(TokenType.iNum, number_str)