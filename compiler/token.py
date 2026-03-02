from dataclasses import dataclass

from compiler.token_type import TokenType


@dataclass(frozen=True)
class Token:
    """Representa um token produzido pelo analisador léxico."""

    type: TokenType
    value: str
    line: int
    column: int
    end_column: int = None

    def __repr__(self) -> str: # Podemos dizer que isso é apenas um log de depuração
        return (
            f"Token(type={self.type.name}, value='{self.value}', "
            f"line={self.line}, column={self.column}, end_column={self.end_column})"
        )
    