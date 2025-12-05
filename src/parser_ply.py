"""Analyseur syntaxique avec PLY (équivalent Python de Bison).

Ce module remplace parser.py en utilisant PLY pour générer le parser.
PLY utilise la même syntaxe que Bison, mais génère du code Python pur.
"""

from __future__ import annotations

import ply.yacc as yacc
from typing import Any

from . import ast
from .errors import ParseError, SourceLocation
from .lexer_ply import lexer, tokens

# Import des tokens depuis le lexer
# (tokens est déjà défini dans lexer_ply.py)


# Grammaire BNF (même grammaire que parser.py)
#
# expression  -> or_expr
# or_expr     -> and_expr (OR and_expr)*
# and_expr    -> not_expr (AND not_expr)*
# not_expr    -> NOT not_expr | primary
# primary     -> IDENT | BOOL | '(' expression ')'


def p_expression(p: yacc.YaccProduction) -> None:
    """expression : or_expr"""
    p[0] = p[1]


def p_or_expr(p: yacc.YaccProduction) -> None:
    """or_expr : and_expr
    | or_expr OR and_expr"""
    if len(p) == 2:
        # or_expr -> and_expr
        p[0] = p[1]
    else:
        # or_expr -> or_expr OR and_expr
        p[0] = ast.Or(left=p[1], right=p[3])


def p_and_expr(p: yacc.YaccProduction) -> None:
    """and_expr : not_expr
    | and_expr AND not_expr"""
    if len(p) == 2:
        # and_expr -> not_expr
        p[0] = p[1]
    else:
        # and_expr -> and_expr AND not_expr
        p[0] = ast.And(left=p[1], right=p[3])


def p_not_expr(p: yacc.YaccProduction) -> None:
    """not_expr : NOT not_expr
    | primary"""
    if len(p) == 2:
        # not_expr -> primary
        p[0] = p[1]
    else:
        # not_expr -> NOT not_expr
        p[0] = ast.Not(expr=p[2])


def p_primary_ident(p: yacc.YaccProduction) -> None:
    """primary : IDENT"""
    p[0] = ast.Var(name=p[1])


def p_primary_bool(p: yacc.YaccProduction) -> None:
    """primary : BOOL"""
    value = p[1].upper() == "TRUE"
    p[0] = ast.BoolLit(value=value)


def p_primary_paren(p: yacc.YaccProduction) -> None:
    """primary : LPAREN expression RPAREN"""
    p[0] = p[2]


# Gestion des erreurs
def p_error(p: yacc.YaccProduction | None) -> None:
    """Gère les erreurs de parsing."""
    if p is None:
        # Erreur à la fin de l'input (token EOF inattendu)
        raise ParseError("Fin d'expression inattendue", source="")
    else:
        # Calculer la colonne (trouver le début de la ligne actuelle)
        line_start = p.lexer.lexdata.rfind("\n", 0, p.lexpos)
        if line_start == -1:
            column = p.lexpos + 1
        else:
            column = p.lexpos - line_start
        location = SourceLocation(
            line=p.lineno,
            column=column,
            offset=p.lexpos,
        )
        raise ParseError(
            f"Token inattendu '{p.value}' (type: {p.type})",
            location=location,
            source=p.lexer.lexdata,
        )


# Créer le parser
parser = yacc.yacc(debug=False, write_tables=False)


def parse(source: str, debug: bool = False) -> ast.Expr:
    """Parse une expression avec PLY.

    Args:
        source: Code source à parser
        debug: Si True, active le mode debug du parser

    Returns:
        L'AST de l'expression

    Raises:
        ParseError: Si une erreur de syntaxe est rencontrée
    """
    # Réinitialiser le lexer
    lexer.input(source)

    # Parser
    try:
        result = parser.parse(source, lexer=lexer, debug=debug)
        if result is None:
            raise ParseError("Erreur de parsing : résultat vide", source=source)
        return result
    except Exception as e:
        if isinstance(e, ParseError):
            raise
        raise ParseError(f"Erreur de parsing : {e}", source=source) from e


if __name__ == "__main__":
    # Test du parser
    test_cases = [
        "A AND B",
        "A OR B",
        "NOT A",
        "(A OR B) AND C",
        "NOT (A AND B)",
        "TRUE AND FALSE",
        "A OR TRUE",
    ]

    print("Tests du parser PLY:\n")
    for test in test_cases:
        try:
            result = parse(test)
            print(f"✓ {test:30} -> {result}")
        except Exception as e:
            print(f"✗ {test:30} -> ERREUR: {e}")

