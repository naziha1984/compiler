"""Analyseur syntaxique (parser) récursif descendant pour le langage logique.

Ce module implémente un parser robuste avec :
- Support lookahead (peek(k))
- Erreurs spécialisées avec messages contextuels
- Mode debug pour tracer les règles de parsing
- Messages d'erreur avec ligne/colonne
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Sequence

from . import ast
from .errors import (
    EndOfInputError,
    LexicalError,
    MissingOperandError,
    MissingParenthesisError,
    ParseError,
    SourceLocation,
    UnexpectedTokenError,
)
from .tokenizer import Token, TokenType, tokenize

logger = logging.getLogger(__name__)


@dataclass
class Parser:
    """Parser récursif descendant avec lookahead et gestion d'erreurs avancée."""

    tokens: Sequence[Token]
    source: str
    current: int = 0
    debug: bool = False

    def _peek(self, k: int = 0) -> Token:
        """Regarde le token à k positions d'avance (lookahead).

        Args:
            k: Nombre de positions à avancer (0 = token actuel)

        Returns:
            Le token à la position current + k
        """
        pos = self.current + k
        if pos >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[pos]

    def _advance(self) -> Token:
        """Avance d'un token et retourne le token précédent."""
        if not self._is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]

    def _is_at_end(self) -> bool:
        """Vérifie si on est à la fin des tokens."""
        return self._peek().type == TokenType.EOF

    def _check(self, token_type: TokenType) -> bool:
        """Vérifie si le token actuel est du type donné."""
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _match(self, *types: TokenType) -> bool:
        """Vérifie si le token actuel correspond à l'un des types donnés et avance si oui."""
        for t in types:
            if self._check(t):
                if self.debug:
                    logger.debug(f"  [MATCH] {t.name}")
                self._advance()
                return True
        return False

    def _consume(
        self,
        token_type: TokenType,
        expected: str | None = None,
    ) -> Token:
        """Consomme un token du type attendu ou lève une erreur.

        Args:
            token_type: Type de token attendu
            expected: Message d'erreur personnalisé (optionnel)

        Returns:
            Le token consommé

        Raises:
            UnexpectedTokenError: Si le token n'est pas du type attendu
        """
        if self._check(token_type):
            return self._advance()

        token = self._peek()
        expected_str = expected or token_type.name
        raise UnexpectedTokenError(
            expected=expected_str,
            found=f"{token.type.name}('{token.lexeme}')",
            location=token.location,
            source=self.source,
        )

    def _error_location(self) -> SourceLocation:
        """Retourne la location du token actuel pour les erreurs."""
        return self._peek().location

    # API publique - méthodes de parsing

    def parse_expression(self) -> ast.Expr:
        """Point d'entrée principal pour l'analyse.

        Grammaire (avec précédence) :

        expression  -> or ;
        or          -> and ( OR and )* ;
        and         -> not ( AND not )* ;
        not         -> NOT not | primary ;
        primary     -> IDENT | BOOL | '(' expression ')' ;

        Returns:
            L'AST de l'expression

        Raises:
            ParseError: Si une erreur de syntaxe est rencontrée
        """
        if self.debug:
            logger.debug("[ENTER] parse_expression")
        expr = self.parse_or()
        if not self._is_at_end():
            token = self._peek()
            raise UnexpectedTokenError(
                expected="fin d'expression",
                found=f"{token.type.name}('{token.lexeme}')",
                location=token.location,
                source=self.source,
            )
        if self.debug:
            logger.debug("[EXIT] parse_expression")
        return expr

    def parse_or(self) -> ast.Expr:
        """Parse une expression OR (priorité la plus faible)."""
        if self.debug:
            logger.debug("[ENTER] parse_or")
        expr = self.parse_and()

        while self._match(TokenType.OR):
            if self.debug:
                logger.debug("  [REDUCE] OR")
            right = self.parse_and()
            expr = ast.Or(left=expr, right=right)

        if self.debug:
            logger.debug("[EXIT] parse_or")
        return expr

    def parse_and(self) -> ast.Expr:
        """Parse une expression AND."""
        if self.debug:
            logger.debug("[ENTER] parse_and")
        expr = self.parse_not()

        while self._match(TokenType.AND):
            if self.debug:
                logger.debug("  [REDUCE] AND")
            right = self.parse_not()
            expr = ast.And(left=expr, right=right)

        if self.debug:
            logger.debug("[EXIT] parse_and")
        return expr

    def parse_not(self) -> ast.Expr:
        """Parse une expression NOT (priorité la plus forte)."""
        if self.debug:
            logger.debug("[ENTER] parse_not")
        if self._match(TokenType.NOT):
            if self.debug:
                logger.debug("  [REDUCE] NOT")
            operand = self.parse_not()  # NOT est associatif à droite
            expr = ast.Not(expr=operand)
            if self.debug:
                logger.debug("[EXIT] parse_not")
            return expr
        expr = self.parse_primary()
        if self.debug:
            logger.debug("[EXIT] parse_not")
        return expr

    def parse_primary(self) -> ast.Expr:
        """Parse un élément primaire (identifiant, booléen, ou parenthèse)."""
        if self.debug:
            logger.debug("[ENTER] parse_primary")
        token = self._peek()

        if self._match(TokenType.BOOL):
            value = token.lexeme.upper() == "TRUE"
            if self.debug:
                logger.debug(f"  [REDUCE] BOOL({value})")
            return ast.BoolLit(value=value)

        if self._match(TokenType.IDENT):
            if self.debug:
                logger.debug(f"  [REDUCE] IDENT({token.lexeme})")
            return ast.Var(name=token.lexeme)

        if self._match(TokenType.LPAREN):
            if self.debug:
                logger.debug("  [REDUCE] LPAREN")
            expr = self.parse_or()
            try:
                self._consume(TokenType.RPAREN, "parenthèse fermante ')'")
            except UnexpectedTokenError as e:
                # Convertir en MissingParenthesisError
                raise MissingParenthesisError(
                    kind="fermante",
                    location=e.location,
                    source=self.source,
                ) from e
            if self.debug:
                logger.debug("[EXIT] parse_primary")
            return expr

        # Erreur : token primaire inattendu
        if self._is_at_end():
            raise EndOfInputError(
                expected="identifiant, booléen, ou parenthèse ouvrante",
                location=self._error_location(),
                source=self.source,
            )

        raise UnexpectedTokenError(
            expected=["identifiant", "booléen (TRUE/FALSE)", "parenthèse ouvrante ('(')"],
            found=f"{token.type.name}('{token.lexeme}')",
            location=token.location,
            source=self.source,
        )


def parse(source: str, debug: bool = False) -> ast.Expr:
    """Fonction utilitaire : tokenise puis parse une chaîne source.

    Args:
        source: Code source à parser
        debug: Si True, active le mode debug du parser

    Returns:
        L'AST de l'expression

    Raises:
        ParseError: Si une erreur de syntaxe est rencontrée
        LexicalError: Si une erreur lexicale est rencontrée
    """
    try:
        tokens: List[Token] = tokenize(source)
    except Exception as e:
        if isinstance(e, LexicalError):
            raise
        raise ParseError(f"Erreur lexicale : {e}", source=source) from e

    parser = Parser(tokens=tokens, source=source, debug=debug)
    return parser.parse_expression()
