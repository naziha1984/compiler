"""Tests pour l'optimizer avec constant folding."""

from src import ast
from src.optimizer import optimize
from src.parser import parse


def test_optimize_not_true():
    expr = parse("NOT TRUE")
    optimized = optimize(expr)
    assert isinstance(optimized, ast.BoolLit)
    assert optimized.value is False


def test_optimize_not_false():
    expr = parse("NOT FALSE")
    optimized = optimize(expr)
    assert isinstance(optimized, ast.BoolLit)
    assert optimized.value is True


def test_optimize_double_not():
    expr = parse("NOT NOT A")
    optimized = optimize(expr)
    assert isinstance(optimized, ast.Var)
    assert optimized.name == "A"


def test_optimize_true_and_x():
    expr = parse("TRUE AND A")
    optimized = optimize(expr)
    assert isinstance(optimized, ast.Var)
    assert optimized.name == "A"


def test_optimize_false_and_x():
    expr = parse("FALSE AND A")
    optimized = optimize(expr)
    assert isinstance(optimized, ast.BoolLit)
    assert optimized.value is False


def test_optimize_x_and_true():
    expr = parse("A AND TRUE")
    optimized = optimize(expr)
    assert isinstance(optimized, ast.Var)
    assert optimized.name == "A"


def test_optimize_x_and_false():
    expr = parse("A AND FALSE")
    optimized = optimize(expr)
    assert isinstance(optimized, ast.BoolLit)
    assert optimized.value is False


def test_optimize_true_or_x():
    expr = parse("TRUE OR A")
    optimized = optimize(expr)
    assert isinstance(optimized, ast.BoolLit)
    assert optimized.value is True


def test_optimize_false_or_x():
    expr = parse("FALSE OR A")
    optimized = optimize(expr)
    assert isinstance(optimized, ast.Var)
    assert optimized.name == "A"


def test_optimize_complex_expression():
    expr = parse("TRUE AND (FALSE OR A)")
    optimized = optimize(expr)
    # TRUE AND X → X, donc on devrait avoir (FALSE OR A)
    # Mais FALSE OR A → A (FALSE OR X → X)
    # Donc le résultat final devrait être A
    assert isinstance(optimized, ast.Var)
    assert optimized.name == "A"


def test_optimize_no_change():
    # Expression qui ne peut pas être optimisée
    expr = parse("A AND B")
    optimized = optimize(expr)
    # Devrait rester identique (structure)
    assert isinstance(optimized, ast.And)
    assert optimized == expr  # Utilise __eq__

