"""Optimiseur d'AST avec constant folding.

Ce module implémente un optimiseur qui applique des règles de simplification :
- NOT TRUE → FALSE
- NOT FALSE → TRUE
- TRUE AND X → X
- FALSE AND X → FALSE
- TRUE OR X → TRUE
- FALSE OR X → X
- NOT NOT X → X
"""

from __future__ import annotations

import logging

from . import ast
from .visitors import ExprVisitor

logger = logging.getLogger(__name__)


class Optimizer(ExprVisitor[ast.Expr]):
    """Visiteur qui optimise l'AST en appliquant des règles de constant folding."""

    def __init__(self, debug: bool = False) -> None:
        """Initialise l'optimiseur.

        Args:
            debug: Si True, log les optimisations effectuées
        """
        self.debug = debug

    def optimize(self, expr: ast.Expr) -> ast.Expr:
        """Optimise une expression AST.

        Args:
            expr: L'expression à optimiser

        Returns:
            L'expression optimisée
        """
        return expr.accept(self)

    def visit_var(self, expr: ast.Var) -> ast.Expr:
        """Les variables ne peuvent pas être optimisées."""
        return expr

    def visit_bool_lit(self, expr: ast.BoolLit) -> ast.Expr:
        """Les littéraux booléens ne peuvent pas être optimisés."""
        return expr

    def visit_not(self, expr: ast.Not) -> ast.Expr:
        """Optimise NOT selon les règles :
        - NOT TRUE → FALSE
        - NOT FALSE → TRUE
        - NOT NOT X → X (double négation)
        """
        operand = expr.expr.accept(self)

        # NOT TRUE → FALSE
        if isinstance(operand, ast.BoolLit) and operand.value:
            if self.debug:
                logger.debug("  [OPT] NOT TRUE → FALSE")
            return ast.BoolLit(value=False)

        # NOT FALSE → TRUE
        if isinstance(operand, ast.BoolLit) and not operand.value:
            if self.debug:
                logger.debug("  [OPT] NOT FALSE → TRUE")
            return ast.BoolLit(value=True)

        # NOT NOT X → X (double négation)
        if isinstance(operand, ast.Not):
            if self.debug:
                logger.debug("  [OPT] NOT NOT X → X")
            return operand.expr

        # Pas d'optimisation possible
        if operand is not expr.expr:
            return ast.Not(expr=operand)
        return expr

    def visit_and(self, expr: ast.And) -> ast.Expr:
        """Optimise AND selon les règles :
        - TRUE AND X → X
        - FALSE AND X → FALSE
        - X AND TRUE → X
        - X AND FALSE → FALSE
        """
        left = expr.left.accept(self)
        right = expr.right.accept(self)

        # TRUE AND X → X
        if isinstance(left, ast.BoolLit) and left.value:
            if self.debug:
                logger.debug("  [OPT] TRUE AND X → X")
            return right

        # FALSE AND X → FALSE
        if isinstance(left, ast.BoolLit) and not left.value:
            if self.debug:
                logger.debug("  [OPT] FALSE AND X → FALSE")
            return ast.BoolLit(value=False)

        # X AND TRUE → X
        if isinstance(right, ast.BoolLit) and right.value:
            if self.debug:
                logger.debug("  [OPT] X AND TRUE → X")
            return left

        # X AND FALSE → FALSE
        if isinstance(right, ast.BoolLit) and not right.value:
            if self.debug:
                logger.debug("  [OPT] X AND FALSE → FALSE")
            return ast.BoolLit(value=False)

        # Pas d'optimisation possible
        if left is not expr.left or right is not expr.right:
            return ast.And(left=left, right=right)
        return expr

    def visit_or(self, expr: ast.Or) -> ast.Expr:
        """Optimise OR selon les règles :
        - TRUE OR X → TRUE
        - FALSE OR X → X
        - X OR TRUE → TRUE
        - X OR FALSE → X
        """
        left = expr.left.accept(self)
        right = expr.right.accept(self)

        # TRUE OR X → TRUE
        if isinstance(left, ast.BoolLit) and left.value:
            if self.debug:
                logger.debug("  [OPT] TRUE OR X → TRUE")
            return ast.BoolLit(value=True)

        # FALSE OR X → X
        if isinstance(left, ast.BoolLit) and not left.value:
            if self.debug:
                logger.debug("  [OPT] FALSE OR X → X")
            return right

        # X OR TRUE → TRUE
        if isinstance(right, ast.BoolLit) and right.value:
            if self.debug:
                logger.debug("  [OPT] X OR TRUE → TRUE")
            return ast.BoolLit(value=True)

        # X OR FALSE → X
        if isinstance(right, ast.BoolLit) and not right.value:
            if self.debug:
                logger.debug("  [OPT] X OR FALSE → X")
            return left

        # Pas d'optimisation possible
        if left is not expr.left or right is not expr.right:
            return ast.Or(left=left, right=right)
        return expr


def optimize(expr: ast.Expr, debug: bool = False) -> ast.Expr:
    """Fonction utilitaire pour optimiser une expression AST.

    Args:
        expr: L'expression à optimiser
        debug: Si True, log les optimisations effectuées

    Returns:
        L'expression optimisée
    """
    optimizer = Optimizer(debug=debug)
    return optimizer.optimize(expr)

