from dataclasses import dataclass

from compiler.token_type import TokenType


@dataclass(frozen=True)
class Token:
    """Representa um token produzido pelo analisador léxico."""

    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self) -> str:
        return (
            f"Token(type={self.type.name}, value='{self.value}', "
            f"line={self.line}, column={self.column})"
        )