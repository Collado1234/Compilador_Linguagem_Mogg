class ScannerError(Exception):
    """Erro léxico com posição na entrada."""

    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Erro na linha {line}, coluna {column}: {message}")
        self.message = message
        self.line = line
        self.column = column


class ParserError(Exception):
    """Erro sintático com posição na entrada."""

    def __init__(self, message: str, line: int, column: int, token=None):
        super().__init__(f"Erro na linha {line}, coluna {column}: {message}")
        self.message = message
        self.line = line
        self.column = column
        self.token = token