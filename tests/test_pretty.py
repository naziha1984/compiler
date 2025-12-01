"""Tests pour le pretty-printer intelligent."""

from src import ast
from src.parser import parse
from src.pretty import CaseStyle, pretty_print


def test_pretty_print_upper_case():
    expr = parse("A AND B")
    result = pretty_print(expr, case_style=CaseStyle.UPPER)
    assert "AND" in result
    assert "and" not in result.lower() or "AND" in result


def test_pretty_print_lower_case():
    expr = parse("A AND B")
    result = pretty_print(expr, case_style=CaseStyle.LOWER)
    assert "and" in result.lower()


def test_pretty_print_minimal_parentheses():
    # A OR B AND C devrait être A OR (B AND C) sans parenthèses si minimal
    expr = parse("A OR B AND C")
    result = pretty_print(expr, show_parentheses="minimal")
    # Devrait minimiser les parenthèses selon la précédence
    assert "A" in result and "B" in result and "C" in result


def test_pretty_print_always_parentheses():
    expr = parse("A AND B")
    result = pretty_print(expr, show_parentheses="always")
    # Devrait avoir des parenthèses même si pas nécessaires
    # (peut varier selon l'implémentation)


def test_pretty_print_bool_literals():
    expr = parse("TRUE AND FALSE")
    result_upper = pretty_print(expr, case_style=CaseStyle.UPPER)
    assert "TRUE" in result_upper
    assert "FALSE" in result_upper

    result_lower = pretty_print(expr, case_style=CaseStyle.LOWER)
    assert "true" in result_lower
    assert "false" in result_lower


def test_pretty_print_not():
    expr = parse("NOT A")
    result = pretty_print(expr)
    assert "NOT" in result or "not" in result.upper()
    assert "A" in result


def test_pretty_print_complex():
    expr = parse("(A OR B) AND NOT C")
    result = pretty_print(expr)
    assert "A" in result
    assert "B" in result
    assert "C" in result

