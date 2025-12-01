"""Analyseur lexical (tokenizer/lexer) pour le langage d'expressions logiques.

Ce module implémente un lexer robuste avec :
- Tracking de ligne/colonne pour chaque token
- Support des commentaires (# ...)
- Messages d'erreur contextuels avec affichage style GCC/Clang
- Mode debug pour afficher les tokens générés
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable, List

from .errors import LexicalError, SourceLocation


class TokenType(Enum):
    """Types de tokens du langage."""

    IDENT = auto()
    BOOL = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    """Représente un token avec sa position dans le code source."""

    type: TokenType
    lexeme: str
    location: SourceLocation  # Position (ligne, colonne, offset)

    @property
    def position(self) -> int:
        """Compatibilité avec l'ancienne API (offset)."""
        return self.location.offset

    def __str__(self) -> str:
        return f"{self.type.name}({self.lexeme!r})@{self.location}"


# Patterns regex pour le lexing
_IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_WHITESPACE_RE = re.compile(r"\s+")
_COMMENT_RE = re.compile(r"#.*")  # Commentaire jusqu'à la fin de la ligne

# Mots-clés du langage (insensibles à la casse)
_KEYWORDS = {
    "AND": TokenType.AND,
    "OR": TokenType.OR,
    "NOT": TokenType.NOT,
    "TRUE": TokenType.BOOL,
    "FALSE": TokenType.BOOL,
}


class Lexer:
    """Analyseur lexical avec tracking de ligne/colonne."""

    def __init__(self, source: str, enable_comments: bool = True) -> None:
        """Initialise le lexer.

        Args:
            source: Code source à tokeniser
            enable_comments: Si True, les commentaires (# ...) sont ignorés
        """
        self.source = source
        self.enable_comments = enable_comments
        self.offset = 0
        self.line = 1
        self.column = 1
        self.length = len(source)

    def _current_location(self) -> SourceLocation:
        """Retourne la position actuelle dans le code source."""
        return SourceLocation(line=self.line, column=self.column, offset=self.offset)

    def _advance(self, count: int = 1) -> None:
        """Avance le curseur de `count` caractères."""
        for _ in range(count):
            if self.offset < self.length:
                if self.source[self.offset] == "\n":
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.offset += 1

    def _match_regex(self, pattern: re.Pattern[str]) -> re.Match[str] | None:
        """Tente de matcher un pattern regex à la position actuelle."""
        return pattern.match(self.source, self.offset)

    def _skip_whitespace(self) -> None:
        """Saute les espaces blancs."""
        while self.offset < self.length:
            m = self._match_regex(_WHITESPACE_RE)
            if m:
                self._advance(m.end() - m.start())
            else:
                break

    def _skip_comment(self) -> bool:
        """Saute un commentaire si présent. Retourne True si un commentaire a été sauté."""
        if not self.enable_comments:
            return False
        m = self._match_regex(_COMMENT_RE)
        if m:
            self._advance(m.end() - m.start())
            return True
        return False

    def _read_token(self) -> Token | None:
        """Lit le prochain token. Retourne None si EOF."""
        # Sauter espaces et commentaires
        while True:
            self._skip_whitespace()
            if not self._skip_comment():
                break

        if self.offset >= self.length:
            return Token(TokenType.EOF, "", self._current_location())

        location = self._current_location()
        ch = self.source[self.offset]

        # Parenthèses
        if ch == "(":
            self._advance()
            return Token(TokenType.LPAREN, "(", location)
        if ch == ")":
            self._advance()
            return Token(TokenType.RPAREN, ")", location)

        # Identifiants / mots-clés
        m = self._match_regex(_IDENT_RE)
        if m:
            lexeme = m.group(0)
            upper = lexeme.upper()
            token_type = _KEYWORDS.get(upper, TokenType.IDENT)
            # Pour les identifiants, on garde la casse originale
            final_lexeme = upper if token_type != TokenType.IDENT else lexeme
            self._advance(len(lexeme))
            return Token(token_type, final_lexeme, location)

        # Rien ne correspond - erreur lexicale
        raise LexicalError(
            f"Caractère inattendu '{ch}'",
            location=location,
            source=self.source,
        )

    def tokenize(self) -> List[Token]:
        """Tokenise le code source et retourne la liste des tokens."""
        tokens: List[Token] = []
        while True:
            token = self._read_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens


def tokenize(source: str, enable_comments: bool = True) -> List[Token]:
    """Fonction utilitaire pour tokeniser une chaîne source.

    Args:
        source: Code source à tokeniser
        enable_comments: Si True, les commentaires (# ...) sont ignorés

    Returns:
        Liste des tokens

    Raises:
        LexicalError: Si un caractère invalide est rencontré
    """
    lexer = Lexer(source, enable_comments=enable_comments)
    return lexer.tokenize()


def debug_tokens(tokens: Iterable[Token]) -> str:
    """Retourne une représentation lisible d'une séquence de tokens pour le debug.

    Args:
        tokens: Séquence de tokens à afficher

    Returns:
        Chaîne formatée avec tous les tokens
    """
    parts = []
    for token in tokens:
        if token.type == TokenType.EOF:
            parts.append(f"EOF@{token.location}")
        else:
            parts.append(f"{token.type.name}({token.lexeme!r})@{token.location}")
    return ", ".join(parts)


def format_lexical_error(error: LexicalError) -> str:
    """Formate une erreur lexicale avec contexte (style GCC/Clang).

    Args:
        error: L'erreur lexicale à formater

    Returns:
        Message d'erreur formaté avec contexte
    """
    return error.format_error()
