"""Évaluateur d'expressions booléennes avec gestion d'erreurs avancée.

Ce module implémente un évaluateur robuste avec :
- Suggestions de variables proches (distance de Levenshtein)
- Mode debug pour tracer l'évaluation
- Messages d'erreur détaillés
"""

from __future__ import annotations

import logging
from typing import Mapping

from . import ast
from .errors import UnknownVariableError
from .visitors import ExprVisitor

logger = logging.getLogger(__name__)


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calcule la distance de Levenshtein entre deux chaînes.

    Args:
        s1: Première chaîne
        s2: Deuxième chaîne

    Returns:
        Distance de Levenshtein
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def find_similar_variables(variable_name: str, available_vars: list[str], max_distance: int = 3) -> list[str]:
    """Trouve des variables similaires à celle demandée.

    Args:
        variable_name: Nom de la variable inconnue
        available_vars: Liste des variables disponibles
        max_distance: Distance de Levenshtein maximale acceptée

    Returns:
        Liste des variables similaires, triée par similarité
    """
    candidates = []
    for var in available_vars:
        distance = levenshtein_distance(variable_name.lower(), var.lower())
        if distance <= max_distance:
            candidates.append((distance, var))

    # Trier par distance puis par nom
    candidates.sort(key=lambda x: (x[0], x[1]))
    return [var for _, var in candidates]


class Evaluator(ExprVisitor[bool]):
    """Visiteur d'évaluation d'expressions booléennes."""

    def __init__(self, env: Mapping[str, bool], debug: bool = False) -> None:
        """Initialise l'évaluateur.

        Args:
            env: Environnement de variables (dictionnaire nom -> valeur)
            debug: Si True, log chaque étape d'évaluation
        """
        self._env = env
        self.debug = debug

    def evaluate(self, expr: ast.Expr) -> bool:
        """Évalue une expression booléenne.

        Args:
            expr: L'expression à évaluer

        Returns:
            Résultat booléen de l'évaluation

        Raises:
            UnknownVariableError: Si une variable inconnue est référencée
        """
        result = expr.accept(self)
        assert isinstance(result, bool)
        return result

    def visit_var(self, expr: ast.Var) -> bool:
        """Évalue une variable."""
        if self.debug:
            logger.debug(f"  [EVAL] Variable: {expr.name}")

        if expr.name not in self._env:
            # Trouver des suggestions
            available_vars = list(self._env.keys())
            suggestions = find_similar_variables(expr.name, available_vars)

            raise UnknownVariableError(
                variable_name=expr.name,
                suggestions=suggestions,
            )

        value = self._env[expr.name]
        if not isinstance(value, bool):
            raise TypeError(f"Valeur non booléenne pour '{expr.name}': {value!r}")

        if self.debug:
            logger.debug(f"  [EVAL] {expr.name} = {value}")

        return value

    def visit_bool_lit(self, expr: ast.BoolLit) -> bool:
        """Évalue un littéral booléen."""
        if self.debug:
            logger.debug(f"  [EVAL] BoolLit: {expr.value}")
        return expr.value

    def visit_not(self, expr: ast.Not) -> bool:
        """Évalue une négation."""
        if self.debug:
            logger.debug("  [EVAL] NOT")
        operand = expr.expr.accept(self)
        result = not operand
        if self.debug:
            logger.debug(f"  [EVAL] NOT {operand} = {result}")
        return result

    def visit_and(self, expr: ast.And) -> bool:
        """Évalue une conjonction."""
        if self.debug:
            logger.debug("  [EVAL] AND")
        left = expr.left.accept(self)
        # Évaluation paresseuse possible, mais on évalue les deux pour le debug
        right = expr.right.accept(self)
        result = left and right
        if self.debug:
            logger.debug(f"  [EVAL] {left} AND {right} = {result}")
        return result

    def visit_or(self, expr: ast.Or) -> bool:
        """Évalue une disjonction."""
        if self.debug:
            logger.debug("  [EVAL] OR")
        left = expr.left.accept(self)
        # Évaluation paresseuse possible, mais on évalue les deux pour le debug
        right = expr.right.accept(self)
        result = left or right
        if self.debug:
            logger.debug(f"  [EVAL] {left} OR {right} = {result}")
        return result


def evaluate(expr: ast.Expr, env: Mapping[str, bool], debug: bool = False) -> bool:
    """Fonction utilitaire pour évaluer une expression booléenne.

    Args:
        expr: L'expression à évaluer
        env: Environnement de variables
        debug: Si True, active le mode debug

    Returns:
        Résultat booléen de l'évaluation

    Raises:
        UnknownVariableError: Si une variable inconnue est référencée
    """
    return Evaluator(env, debug=debug).evaluate(expr)
