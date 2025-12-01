"""Pretty-printer intelligent pour l'AST avec minimisation de parenthèses.

Ce module implémente un pretty-printer avancé qui :
- Minimise intelligemment les parenthèses selon la précédence
- Respecte l'associativité des opérateurs
- Supporte des options de formatage (casse, indentation, etc.)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from . import ast
from .visitors import ExprVisitor


class CaseStyle(Enum):
    """Style de casse pour les mots-clés."""

    UPPER = "upper"  # AND, OR, NOT
    LOWER = "lower"  # and, or, not
    MIXED = "mixed"  # And, Or, Not


@dataclass
class PrettyOptions:
    """Options de formatage pour le pretty-printer."""

    case_style: CaseStyle = CaseStyle.UPPER
    show_parentheses: str = "minimal"  # "always", "minimal", "never"
    indent: int = 0  # Indentation pour les expressions multi-lignes (0 = une ligne)


class SmartPrettyPrinter(ExprVisitor[str]):
    """Pretty-printer intelligent qui minimise les parenthèses."""

    # Priorités des opérateurs (plus élevé = plus prioritaire)
    PREC_NOT = 3
    PREC_AND = 2
    PREC_OR = 1
    PREC_PAREN = 0  # Parenthèses explicites

    def __init__(self, options: PrettyOptions | None = None) -> None:
        """Initialise le pretty-printer.

        Args:
            options: Options de formatage
        """
        self.options = options or PrettyOptions()
        self._parent_precedence = self.PREC_PAREN  # Contexte de précédence parent

    def format(self, expr: ast.Expr) -> str:
        """Formate une expression AST en chaîne lisible.

        Args:
            expr: L'expression à formater

        Returns:
            Chaîne formatée
        """
        self._parent_precedence = self.PREC_PAREN
        return expr.accept(self)

    def _format_keyword(self, keyword: str) -> str:
        """Formate un mot-clé selon le style de casse."""
        if self.options.case_style == CaseStyle.UPPER:
            return keyword.upper()
        elif self.options.case_style == CaseStyle.LOWER:
            return keyword.lower()
        else:  # MIXED
            return keyword.capitalize()

    def _format_bool(self, value: bool) -> str:
        """Formate un booléen selon le style de casse."""
        if self.options.case_style == CaseStyle.UPPER:
            return "TRUE" if value else "FALSE"
        elif self.options.case_style == CaseStyle.LOWER:
            return "true" if value else "false"
        else:  # MIXED
            return "True" if value else "False"

    def _needs_parens(self, expr_precedence: int) -> bool:
        """Détermine si des parenthèses sont nécessaires selon la précédence."""
        if self.options.show_parentheses == "always":
            return True
        if self.options.show_parentheses == "never":
            return False
        # "minimal" : parenthèses seulement si nécessaire
        return expr_precedence < self._parent_precedence

    def _wrap_if_needed(self, s: str, expr_precedence: int) -> str:
        """Enveloppe une expression dans des parenthèses si nécessaire."""
        if self._needs_parens(expr_precedence):
            return f"({s})"
        return s

    def visit_var(self, expr: ast.Var) -> str:
        return expr.name

    def visit_bool_lit(self, expr: ast.BoolLit) -> str:
        return self._format_bool(expr.value)

    def visit_not(self, expr: ast.Not) -> str:
        not_keyword = self._format_keyword("NOT")
        # NOT a la priorité la plus élevée
        old_prec = self._parent_precedence
        self._parent_precedence = self.PREC_NOT
        operand_str = expr.expr.accept(self)
        self._parent_precedence = old_prec

        # Si l'opérande est un NOT, on peut avoir besoin de parenthèses
        # selon les options
        if isinstance(expr.expr, ast.Not) and self._needs_parens(self.PREC_NOT):
            operand_str = f"({operand_str})"

        return f"{not_keyword} {operand_str}"

    def visit_and(self, expr: ast.And) -> str:
        and_keyword = self._format_keyword("AND")
        old_prec = self._parent_precedence
        self._parent_precedence = self.PREC_AND

        # Visiter les opérandes avec la précédence AND
        left_str = expr.left.accept(self)
        right_str = expr.right.accept(self)

        self._parent_precedence = old_prec

        # Vérifier si les opérandes ont besoin de parenthèses
        if isinstance(expr.left, (ast.Or)) and self._needs_parens(self.PREC_OR):
            left_str = f"({left_str})"
        if isinstance(expr.right, (ast.Or)) and self._needs_parens(self.PREC_OR):
            right_str = f"({right_str})"

        result = f"{left_str} {and_keyword} {right_str}"
        return self._wrap_if_needed(result, self.PREC_AND)

    def visit_or(self, expr: ast.Or) -> str:
        or_keyword = self._format_keyword("OR")
        old_prec = self._parent_precedence
        self._parent_precedence = self.PREC_OR

        # Visiter les opérandes avec la précédence OR
        left_str = expr.left.accept(self)
        right_str = expr.right.accept(self)

        self._parent_precedence = old_prec

        result = f"{left_str} {or_keyword} {right_str}"
        return self._wrap_if_needed(result, self.PREC_OR)


def pretty_print(
    expr: ast.Expr,
    case_style: CaseStyle | str = CaseStyle.UPPER,
    show_parentheses: str = "minimal",
    indent: int = 0,
) -> str:
    """Fonction utilitaire pour formater une expression AST.

    Args:
        expr: L'expression à formater
        case_style: Style de casse ("upper", "lower", "mixed")
        show_parentheses: Mode d'affichage des parenthèses ("always", "minimal", "never")
        indent: Indentation (non utilisé pour l'instant, réservé pour version multi-lignes)

    Returns:
        Chaîne formatée
    """
    if isinstance(case_style, str):
        case_style = CaseStyle(case_style.lower())

    options = PrettyOptions(
        case_style=case_style,
        show_parentheses=show_parentheses,
        indent=indent,
    )
    printer = SmartPrettyPrinter(options=options)
    return printer.format(expr)

