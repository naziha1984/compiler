"""Tests pour le parser amélioré."""

import pytest

from src import ast
from src.errors import (
    EndOfInputError,
    MissingParenthesisError,
    ParseError,
    UnexpectedTokenError,
)
from src.parser import parse


def eval_structure(expr):
    """Petite aide pour distinguer facilement les types lors des assertions."""
    return type(expr).__name__


def test_operator_precedence_not_and_or():
    # NOT > AND > OR
    expr = parse("A OR B AND NOT C")
    # Attendu : Or(A, And(B, Not(C)))
    assert isinstance(expr, ast.Or)
    assert isinstance(expr.left, ast.Var)
    assert expr.left.name == "A"
    assert isinstance(expr.right, ast.And)
    assert isinstance(expr.right.left, ast.Var)
    assert expr.right.left.name == "B"
    assert isinstance(expr.right.right, ast.Not)
    assert isinstance(expr.right.right.expr, ast.Var)
    assert expr.right.right.expr.name == "C"


def test_parentheses_override_precedence():
    expr = parse("(A OR B) AND C")
    # Attendu : And(Or(A,B), C)
    assert isinstance(expr, ast.And)
    assert isinstance(expr.left, ast.Or)
    assert isinstance(expr.left.left, ast.Var)
    assert expr.left.left.name == "A"
    assert isinstance(expr.left.right, ast.Var)
    assert expr.left.right.name == "B"
    assert isinstance(expr.right, ast.Var)
    assert expr.right.name == "C"


def test_nested_not():
    expr = parse("NOT NOT A")
    assert isinstance(expr, ast.Not)
    assert isinstance(expr.expr, ast.Not)
    assert isinstance(expr.expr.expr, ast.Var)
    assert expr.expr.expr.name == "A"


def test_bool_literals():
    expr = parse("TRUE AND FALSE")
    assert isinstance(expr, ast.And)
    assert isinstance(expr.left, ast.BoolLit)
    assert expr.left.value is True
    assert isinstance(expr.right, ast.BoolLit)
    assert expr.right.value is False


def test_unexpected_token_error():
    with pytest.raises(UnexpectedTokenError):
        parse("AND B")  # AND ne peut pas être au début


def test_missing_closing_parenthesis():
    with pytest.raises(MissingParenthesisError) as exc_info:
        parse("(A AND B")
    assert exc_info.value.kind == "fermante"


def test_trailing_garbage_after_expression():
    with pytest.raises(UnexpectedTokenError):
        parse("A AND B C")  # C est inattendu après l'expression


def test_end_of_input_error():
    with pytest.raises(EndOfInputError):
        parse("A AND")  # Fin d'entrée inattendue


def test_parse_debug_mode():
    import logging

    logging.basicConfig(level=logging.DEBUG)
    # Ne devrait pas lever d'erreur
    expr = parse("A AND B", debug=True)
    assert isinstance(expr, ast.And)


def test_complex_expression():
    expr = parse("(A OR B) AND (NOT C OR D)")
    assert isinstance(expr, ast.And)
    assert isinstance(expr.left, ast.Or)
    assert isinstance(expr.right, ast.Or)
