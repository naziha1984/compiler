"""Tests pour la sérialisation JSON de l'AST."""

import json

from src import ast
from src.ast import from_json
from src.parser import parse


def test_ast_to_json():
    expr = parse("A AND B")
    json_data = expr.to_json()
    assert isinstance(json_data, dict)
    assert json_data["type"] == "And"
    assert "left" in json_data
    assert "right" in json_data


def test_ast_from_json():
    json_data = {
        "type": "And",
        "left": {"type": "Var", "name": "A"},
        "right": {"type": "Var", "name": "B"},
    }
    expr = from_json(json_data)
    assert isinstance(expr, ast.And)
    assert isinstance(expr.left, ast.Var)
    assert expr.left.name == "A"
    assert isinstance(expr.right, ast.Var)
    assert expr.right.name == "B"


def test_ast_json_roundtrip():
    original = parse("(A OR B) AND NOT C")
    json_str = json.dumps(original.to_json())
    json_data = json.loads(json_str)
    restored = from_json(json_data)
    # Vérifier l'égalité structurelle
    assert restored == original


def test_ast_eq():
    expr1 = parse("A AND B")
    expr2 = parse("A AND B")
    assert expr1 == expr2

    expr3 = parse("A OR B")
    assert expr1 != expr3


def test_bool_lit_json():
    expr = ast.BoolLit(value=True)
    json_data = expr.to_json()
    assert json_data == {"type": "BoolLit", "value": True}


def test_not_json():
    expr = parse("NOT A")
    json_data = expr.to_json()
    assert json_data["type"] == "Not"
    assert json_data["expr"]["type"] == "Var"

