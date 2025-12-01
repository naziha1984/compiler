"""Module centralisé pour toutes les erreurs du compilateur.

Ce module définit toutes les classes d'erreurs spécialisées avec support
pour le tracking de ligne/colonne et l'affichage contextuel.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SourceLocation:
    """Représente une position dans le code source (ligne, colonne, offset)."""

    line: int  # 1-indexed
    column: int  # 1-indexed
    offset: int  # 0-indexed position dans la chaîne

    def __str__(self) -> str:
        return f"{self.line}:{self.column}"


class CompilerError(Exception):
    """Classe de base pour toutes les erreurs du compilateur."""

    def __init__(
        self,
        message: str,
        location: SourceLocation | None = None,
        source: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.location = location
        self.source = source

    def format_error(self, context_lines: int = 2) -> str:
        """Formate l'erreur avec contexte (style GCC/Clang).

        Args:
            context_lines: Nombre de lignes de contexte à afficher

        Returns:
            Message d'erreur formaté avec contexte et flèche pointant l'erreur
        """
        if not self.location or not self.source:
            return str(self.message)

        lines = self.source.splitlines()
        line_num = self.location.line - 1

        if line_num < 0 or line_num >= len(lines):
            return str(self.message)

        error_line = lines[line_num]
        start_line = max(0, line_num - context_lines)
        end_line = min(len(lines), line_num + context_lines + 1)

        parts = [f"{self.__class__.__name__}: {self.message}"]
        parts.append(f"  --> {self.location}")

        # Afficher les lignes de contexte
        for i in range(start_line, end_line):
            marker = ">>>" if i == line_num else "   "
            parts.append(f"{marker} {i + 1:4d} | {lines[i]}")

            # Afficher la flèche pointant l'erreur
            if i == line_num:
                arrow = " " * (self.location.column + 10) + "^" * max(1, len(error_line) - self.location.column + 1)
                parts.append(f"       | {arrow}")

        return "\n".join(parts)


class LexicalError(CompilerError):
    """Erreur levée lorsqu'un caractère ou lexème invalide est rencontré."""

    pass


class ParseError(CompilerError):
    """Classe de base pour toutes les erreurs de parsing."""

    pass


class UnexpectedTokenError(ParseError):
    """Erreur levée lorsqu'un token inattendu est rencontré."""

    def __init__(
        self,
        expected: str | list[str],
        found: str,
        location: SourceLocation | None = None,
        source: str | None = None,
    ) -> None:
        if isinstance(expected, list):
            expected_str = " ou ".join(expected) if len(expected) <= 2 else f"l'un de {expected}"
        else:
            expected_str = expected
        message = f"Token inattendu '{found}', {expected_str} attendu"
        super().__init__(message, location, source)
        self.expected = expected
        self.found = found


class MissingParenthesisError(ParseError):
    """Erreur levée lorsqu'une parenthèse est manquante."""

    def __init__(
        self,
        kind: str,  # "ouvrante" ou "fermante"
        location: SourceLocation | None = None,
        source: str | None = None,
    ) -> None:
        message = f"Parenthèse {kind} manquante"
        super().__init__(message, location, source)
        self.kind = kind


class MissingOperandError(ParseError):
    """Erreur levée lorsqu'un opérande est manquant."""

    def __init__(
        self,
        operator: str,
        location: SourceLocation | None = None,
        source: str | None = None,
    ) -> None:
        message = f"Opérande manquant pour l'opérateur '{operator}'"
        super().__init__(message, location, source)
        self.operator = operator


class EndOfInputError(ParseError):
    """Erreur levée lorsqu'on atteint la fin de l'entrée de manière inattendue."""

    def __init__(
        self,
        expected: str,
        location: SourceLocation | None = None,
        source: str | None = None,
    ) -> None:
        message = f"Fin d'entrée inattendue, {expected} attendu"
        super().__init__(message, location, source)
        self.expected = expected


class EvaluationError(CompilerError):
    """Classe de base pour toutes les erreurs d'évaluation."""

    pass


class UnknownVariableError(EvaluationError):
    """Erreur levée lorsqu'une variable inconnue est référencée."""

    def __init__(
        self,
        variable_name: str,
        suggestions: list[str] | None = None,
        location: SourceLocation | None = None,
        source: str | None = None,
    ) -> None:
        message = f"Variable inconnue '{variable_name}'"
        if suggestions:
            suggestions_str = ", ".join(suggestions[:3])
            message += f". Suggestions: {suggestions_str}"
        super().__init__(message, location, source)
        self.variable_name = variable_name
        self.suggestions = suggestions or []

