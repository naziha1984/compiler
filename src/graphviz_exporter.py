"""Exporteur Graphviz pour visualiser l'AST.

Ce module permet de générer des fichiers .dot (Graphviz) pour visualiser
l'arbre syntaxique abstrait (AST) sous forme de graphe.
"""

from __future__ import annotations

from typing import TextIO

from . import ast
from .visitors import ExprVisitor


class GraphvizExporter(ExprVisitor[int]):
    """Visiteur qui génère une représentation Graphviz de l'AST."""

    def __init__(self, output: TextIO) -> None:
        """Initialise l'exporteur.

        Args:
            output: Fichier ou stream où écrire le code DOT
        """
        self.output = output
        self.node_counter = 0
        self.node_ids: dict[ast.Expr, int] = {}

    def export(self, expr: ast.Expr, graph_name: str = "AST") -> None:
        """Exporte un AST en format Graphviz DOT.

        Args:
            expr: L'expression AST à exporter
            graph_name: Nom du graphe
        """
        self.node_counter = 0
        self.node_ids = {}

        self.output.write(f"digraph {graph_name} {{\n")
        self.output.write("  node [shape=box, style=rounded];\n")
        self.output.write("  edge [fontsize=10];\n\n")

        # Visiter l'AST pour générer les nœuds et arêtes
        root_id = expr.accept(self)

        self.output.write('  root [label="ROOT", shape=ellipse, style=filled, fillcolor=lightblue];\n')
        self.output.write(f"  root -> n{root_id};\n")
        self.output.write("}\n")

    def _get_node_id(self, expr: ast.Expr) -> int:
        """Obtient ou crée un ID unique pour un nœud."""
        if expr not in self.node_ids:
            self.node_counter += 1
            self.node_ids[expr] = self.node_counter
        return self.node_ids[expr]

    def _escape_label(self, text: str) -> str:
        """Échappe les caractères spéciaux pour les labels DOT."""
        # Remplacer les guillemets et caractères spéciaux
        text = text.replace("\\", "\\\\")  # Échapper les backslashes d'abord
        text = text.replace('"', '\\"')    # Échapper les guillemets
        text = text.replace("\n", "\\n")   # Échapper les newlines
        return text

    def visit_var(self, expr: ast.Var) -> int:
        node_id = self._get_node_id(expr)
        # Échapper le nom de la variable
        name_escaped = self._escape_label(expr.name)
        label_text = f"Var\\n{name_escaped}"
        self.output.write(f'  n{node_id} [label="{label_text}"];\n')
        return node_id

    def visit_bool_lit(self, expr: ast.BoolLit) -> int:
        node_id = self._get_node_id(expr)
        value_str = "TRUE" if expr.value else "FALSE"
        label_text = f"BoolLit\\n{value_str}"
        self.output.write(f'  n{node_id} [label="{label_text}", fillcolor=lightgreen, style="rounded,filled"];\n')
        return node_id

    def visit_not(self, expr: ast.Not) -> int:
        node_id = self._get_node_id(expr)
        self.output.write('  n{node_id} [label="NOT", fillcolor=lightyellow, style="rounded,filled"];\n'.format(node_id=node_id))
        operand_id = expr.expr.accept(self)
        self.output.write(f'  n{node_id} -> n{operand_id} [label="expr"];\n')
        return node_id

    def visit_and(self, expr: ast.And) -> int:
        node_id = self._get_node_id(expr)
        self.output.write('  n{node_id} [label="AND", fillcolor=lightcoral, style="rounded,filled"];\n'.format(node_id=node_id))
        left_id = expr.left.accept(self)
        right_id = expr.right.accept(self)
        self.output.write(f'  n{node_id} -> n{left_id} [label="left"];\n')
        self.output.write(f'  n{node_id} -> n{right_id} [label="right"];\n')
        return node_id

    def visit_or(self, expr: ast.Or) -> int:
        node_id = self._get_node_id(expr)
        self.output.write('  n{node_id} [label="OR", fillcolor=lightcyan, style="rounded,filled"];\n'.format(node_id=node_id))
        left_id = expr.left.accept(self)
        right_id = expr.right.accept(self)
        self.output.write(f'  n{node_id} -> n{left_id} [label="left"];\n')
        self.output.write(f'  n{node_id} -> n{right_id} [label="right"];\n')
        return node_id


def export_to_dot(expr: ast.Expr, output: TextIO | str, graph_name: str = "AST") -> None:
    """Exporte un AST en format Graphviz DOT.

    Args:
        expr: L'expression AST à exporter
        output: Fichier ou nom de fichier où écrire le code DOT
        graph_name: Nom du graphe
    """
    if isinstance(output, str):
        with open(output, "w", encoding="utf-8") as f:
            export_to_dot(expr, f, graph_name)
    else:
        exporter = GraphvizExporter(output)
        exporter.export(expr, graph_name)
