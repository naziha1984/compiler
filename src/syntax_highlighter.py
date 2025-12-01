"""Colorisation syntaxique pour les expressions logiques.

Ce module implémente un QSyntaxHighlighter personnalisé pour coloriser
les expressions logiques dans le champ de saisie.
"""

from __future__ import annotations

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QColor, QTextCharFormat, QSyntaxHighlighter


class LogicalExpressionHighlighter(QSyntaxHighlighter):
    """Coloriseur syntaxique pour le langage logique."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setup_highlighting_rules()

    def setup_highlighting_rules(self) -> None:
        """Configure les règles de colorisation."""
        self.highlighting_rules: list[tuple[QRegularExpression, QTextCharFormat]] = []

        # Mots-clés (AND, OR, NOT, TRUE, FALSE) - Bleu clair
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#64B5F6"))  # Bleu clair Material
        keyword_format.setFontWeight(600)
        keywords = ["AND", "OR", "NOT", "TRUE", "FALSE"]
        for keyword in keywords:
            pattern = QRegularExpression(rf"\b{keyword}\b", QRegularExpression.PatternOption.CaseInsensitiveOption)
            self.highlighting_rules.append((pattern, keyword_format))

        # Variables (identifiants) - Blanc
        variable_format = QTextCharFormat()
        variable_format.setForeground(QColor("#FFFFFF"))
        variable_format.setFontWeight(500)
        pattern = QRegularExpression(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
        self.highlighting_rules.append((pattern, variable_format))

        # Parenthèses - Jaune
        paren_format = QTextCharFormat()
        paren_format.setForeground(QColor("#FFC107"))  # Jaune Material
        paren_format.setFontWeight(700)
        pattern = QRegularExpression(r"[()]")
        self.highlighting_rules.append((pattern, paren_format))

        # Commentaires (# ...) - Gris
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#757575"))  # Gris Material
        comment_format.setFontItalic(True)
        pattern = QRegularExpression(r"#.*")
        self.highlighting_rules.append((pattern, comment_format))

    def highlightBlock(self, text: str) -> None:
        """Applique la colorisation à un bloc de texte."""
        for pattern, format_char in self.highlighting_rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format_char)

    def highlight_error(self, position: int, length: int = 1) -> None:
        """Surligne une erreur en rouge."""
        error_format = QTextCharFormat()
        error_format.setForeground(QColor("#F44336"))  # Rouge Material
        error_format.setBackground(QColor("#3D1F1F"))  # Fond rouge foncé
        error_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SingleUnderline)
        error_format.setUnderlineColor(QColor("#F44336"))
        error_format.setFontWeight(700)

        # Trouver le bloc contenant la position
        block = self.document().findBlock(position)
        if block.isValid():
            block_pos = position - block.position()
            self.setFormat(block_pos, length, error_format)

