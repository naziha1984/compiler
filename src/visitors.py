"""Module pour le Visitor Pattern et les classes de base des visiteurs.

Ce module définit l'interface ExprVisitor et des classes utilitaires
pour implémenter des visiteurs sur l'AST.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from . import ast

T = TypeVar("T")


class ExprVisitor(ABC, Generic[T]):
    """Interface pour les visiteurs d'expressions AST.

    Cette classe abstraite définit les méthodes que tout visiteur doit implémenter
    pour parcourir l'AST. Utilisez cette classe comme base pour créer vos propres
    visiteurs (évaluateur, optimizer, pretty-printer, etc.).
    """

    @abstractmethod
    def visit_var(self, expr: ast.Var) -> T:
        """Visite un nœud Var (variable).

        Args:
            expr: Le nœud Var à visiter

        Returns:
            Résultat de la visite (type dépendant de l'implémentation)
        """
        pass

    @abstractmethod
    def visit_bool_lit(self, expr: ast.BoolLit) -> T:
        """Visite un nœud BoolLit (littéral booléen).

        Args:
            expr: Le nœud BoolLit à visiter

        Returns:
            Résultat de la visite
        """
        pass

    @abstractmethod
    def visit_not(self, expr: ast.Not) -> T:
        """Visite un nœud Not (négation).

        Args:
            expr: Le nœud Not à visiter

        Returns:
            Résultat de la visite
        """
        pass

    @abstractmethod
    def visit_and(self, expr: ast.And) -> T:
        """Visite un nœud And (conjonction).

        Args:
            expr: Le nœud And à visiter

        Returns:
            Résultat de la visite
        """
        pass

    @abstractmethod
    def visit_or(self, expr: ast.Or) -> T:
        """Visite un nœud Or (disjonction).

        Args:
            expr: Le nœud Or à visiter

        Returns:
            Résultat de la visite
        """
        pass


class DefaultVisitor(ExprVisitor[T]):
    """Visiteur par défaut qui visite récursivement tous les nœuds.

    Utile comme classe de base pour les visiteurs qui ont besoin d'un comportement
    par défaut pour certains nœuds.
    """

    def visit_var(self, expr: ast.Var) -> T:
        """Visite par défaut : ne fait rien."""
        raise NotImplementedError("visit_var doit être implémenté")

    def visit_bool_lit(self, expr: ast.BoolLit) -> T:
        """Visite par défaut : ne fait rien."""
        raise NotImplementedError("visit_bool_lit doit être implémenté")

    def visit_not(self, expr: ast.Not) -> T:
        """Visite par défaut : visite récursivement l'opérande."""
        return expr.expr.accept(self)

    def visit_and(self, expr: ast.And) -> T:
        """Visite par défaut : visite récursivement les deux opérandes."""
        expr.left.accept(self)
        expr.right.accept(self)
        raise NotImplementedError("visit_and doit retourner une valeur")

    def visit_or(self, expr: ast.Or) -> T:
        """Visite par défaut : visite récursivement les deux opérandes."""
        expr.left.accept(self)
        expr.right.accept(self)
        raise NotImplementedError("visit_or doit retourner une valeur")

