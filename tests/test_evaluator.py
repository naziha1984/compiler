"""Tests pour l'évaluateur amélioré."""

import pytest

from src import ast
from src.evaluator import evaluate, find_similar_variables
from src.errors import UnknownVariableError
from src.parser import parse


def test_evaluate_simple_expression_with_env():
    expr = parse("A AND B")
    result = evaluate(expr, {"A": True, "B": False})
    assert result is False


def test_evaluate_or_and_not_precedence():
    expr = parse("A OR B AND NOT C")
    result = evaluate(expr, {"A": False, "B": True, "C": True})
    # A OR (B AND NOT C) = False OR (True AND False) = False
    assert result is False


def test_evaluate_parentheses():
    expr = parse("(A OR B) AND C")
    result = evaluate(expr, {"A": True, "B": False, "C": True})
    # (True OR False) AND True = True AND True = True
    assert result is True


def test_unknown_variable_raises():
    expr = parse("UNKNOWN")
    with pytest.raises(UnknownVariableError) as exc_info:
        evaluate(expr, {"A": True})
    assert "UNKNOWN" in str(exc_info.value)
    assert exc_info.value.variable_name == "UNKNOWN"


def test_unknown_variable_suggestions():
    expr = parse("UNKNON")  # Faute de frappe de "UNKNOWN"
    env = {"UNKNOWN": True, "OTHER": False}
    with pytest.raises(UnknownVariableError) as exc_info:
        evaluate(expr, env)
    # Devrait suggérer "UNKNOWN" car proche
    assert len(exc_info.value.suggestions) > 0
    assert "UNKNOWN" in exc_info.value.suggestions


def test_find_similar_variables():
    available = ["alpha", "beta", "gamma", "ALPHA"]
    suggestions = find_similar_variables("alpa", available, max_distance=2)
    assert "alpha" in suggestions or "ALPHA" in suggestions


def test_nested_not_evaluation():
    expr = parse("NOT NOT A")
    result = evaluate(expr, {"A": True})
    # NOT NOT True = True
    assert result is True


def test_evaluate_bool_literals():
    expr = parse("TRUE AND FALSE")
    result = evaluate(expr, {})
    assert result is False
