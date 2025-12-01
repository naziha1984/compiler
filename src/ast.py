"""Module définissant l'AST (Abstract Syntax Tree) du langage logique.

Ce module contient :
- Les nœuds AST (Var, BoolLit, Not, And, Or)
- Le Visitor Pattern avec accept()
- Comparaison d'égalité (__eq__)
- Sérialisation JSON (to_json, from_json)
- Pretty-printer de base (déplacé dans pretty.py pour version avancée)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from .visitors import ExprVisitor


@dataclass(frozen=True)
class Var:
    """Nœud AST représentant une variable (identifiant)."""

    name: str

    def accept(self, visitor: ExprVisitor[Any]) -> Any:
        """Accepte un visiteur (Visitor Pattern)."""
        return visitor.visit_var(self)

    def __eq__(self, other: object) -> bool:
        """Comparaison d'égalité."""
        if not isinstance(other, Var):
            return False
        return self.name == other.name

    def to_json(self) -> dict[str, Any]:
        """Sérialise le nœud en JSON."""
        return {"type": "Var", "name": self.name}


@dataclass(frozen=True)
class BoolLit:
    """Nœud AST représentant un littéral booléen (TRUE/FALSE)."""

    value: bool

    def accept(self, visitor: ExprVisitor[Any]) -> Any:
        """Accepte un visiteur (Visitor Pattern)."""
        return visitor.visit_bool_lit(self)

    def __eq__(self, other: object) -> bool:
        """Comparaison d'égalité."""
        if not isinstance(other, BoolLit):
            return False
        return self.value == other.value

    def to_json(self) -> dict[str, Any]:
        """Sérialise le nœud en JSON."""
        return {"type": "BoolLit", "value": self.value}


@dataclass(frozen=True)
class Not:
    """Nœud AST représentant une négation logique (NOT)."""

    expr: Expr

    def accept(self, visitor: ExprVisitor[Any]) -> Any:
        """Accepte un visiteur (Visitor Pattern)."""
        return visitor.visit_not(self)

    def __eq__(self, other: object) -> bool:
        """Comparaison d'égalité."""
        if not isinstance(other, Not):
            return False
        return self.expr == other.expr

    def to_json(self) -> dict[str, Any]:
        """Sérialise le nœud en JSON."""
        return {"type": "Not", "expr": self.expr.to_json()}


@dataclass(frozen=True)
class And:
    """Nœud AST représentant une conjonction logique (AND)."""

    left: Expr
    right: Expr

    def accept(self, visitor: ExprVisitor[Any]) -> Any:
        """Accepte un visiteur (Visitor Pattern)."""
        return visitor.visit_and(self)

    def __eq__(self, other: object) -> bool:
        """Comparaison d'égalité."""
        if not isinstance(other, And):
            return False
        return self.left == other.left and self.right == other.right

    def to_json(self) -> dict[str, Any]:
        """Sérialise le nœud en JSON."""
        return {"type": "And", "left": self.left.to_json(), "right": self.right.to_json()}


@dataclass(frozen=True)
class Or:
    """Nœud AST représentant une disjonction logique (OR)."""

    left: Expr
    right: Expr

    def accept(self, visitor: ExprVisitor[Any]) -> Any:
        """Accepte un visiteur (Visitor Pattern)."""
        return visitor.visit_or(self)

    def __eq__(self, other: object) -> bool:
        """Comparaison d'égalité."""
        if not isinstance(other, Or):
            return False
        return self.left == other.left and self.right == other.right

    def to_json(self) -> dict[str, Any]:
        """Sérialise le nœud en JSON."""
        return {"type": "Or", "left": self.left.to_json(), "right": self.right.to_json()}


# Type union pour toutes les expressions
Expr = Var | BoolLit | Not | And | Or


def from_json(data: dict[str, Any] | str) -> Expr:
    """Désérialise un nœud AST depuis JSON.

    Args:
        data: Dictionnaire JSON ou chaîne JSON

    Returns:
        L'AST désérialisé

    Raises:
        ValueError: Si le format JSON est invalide
    """
    if isinstance(data, str):
        data = json.loads(data)

    node_type = data.get("type")
    if node_type == "Var":
        return Var(name=data["name"])
    elif node_type == "BoolLit":
        return BoolLit(value=data["value"])
    elif node_type == "Not":
        return Not(expr=from_json(data["expr"]))
    elif node_type == "And":
        return And(left=from_json(data["left"]), right=from_json(data["right"]))
    elif node_type == "Or":
        return Or(left=from_json(data["left"]), right=from_json(data["right"]))
    else:
        raise ValueError(f"Type de nœud inconnu : {node_type}")


# Pretty-printer simple (version de base, la version avancée est dans pretty.py)
class ASTPrettyPrinter(ExprVisitor[None]):
    """Pretty-printer simple pour l'AST (affichage lisible et indenté)."""

    def __init__(self) -> None:
        self._lines: list[str] = []
        self._indent_level: int = 0

    def format(self, expr: Expr) -> str:
        """Formate une expression AST en chaîne lisible."""
        self._lines = []
        self._indent_level = 0
        expr.accept(self)
        return "\n".join(self._lines)

    def visit_var(self, expr: Var) -> None:
        self._add_line(f"Var(name={expr.name})")

    def visit_bool_lit(self, expr: BoolLit) -> None:
        self._add_line(f"BoolLit(value={expr.value})")

    def visit_not(self, expr: Not) -> None:
        self._add_line("Not")
        self._with_indent(lambda: expr.expr.accept(self))

    def visit_and(self, expr: And) -> None:
        self._add_line("And")
        self._with_indent(lambda: (expr.left.accept(self), expr.right.accept(self)))

    def visit_or(self, expr: Or) -> None:
        self._add_line("Or")
        self._with_indent(lambda: (expr.left.accept(self), expr.right.accept(self)))

    def _add_line(self, text: str) -> None:
        indent = "  " * self._indent_level
        self._lines.append(f"{indent}{text}")

    def _with_indent(self, func) -> None:
        self._indent_level += 1
        try:
            func()
        finally:
            self._indent_level -= 1


def pretty_print(expr: Expr) -> str:
    """Fonction utilitaire de pretty-printing (version simple).

    Pour une version avancée avec minimisation de parenthèses, utilisez pretty.py.
    """
    printer = ASTPrettyPrinter()
    return printer.format(expr)
