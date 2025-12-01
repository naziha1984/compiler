"""Fenêtre "À propos" pour l'application de compilateur logique."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout


class AboutDialog(QDialog):
    """Fenêtre de dialogue "À propos"."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("À propos du Compilateur de Langage Logique")
        self.setFixedSize(500, 400)
        self.init_ui()

    def init_ui(self) -> None:
        """Initialise l'interface de la fenêtre."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Titre
        title = QLabel("Compilateur de Langage Logique")
        title_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Version
        version = QLabel("Version 2.0.0")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version.setStyleSheet("color: #888888;")
        layout.addWidget(version)

        # Séparateur
        separator = QLabel("─" * 50)
        separator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        separator.setStyleSheet("color: #444444;")
        layout.addWidget(separator)

        # Description
        description = QLabel(
            "Un compilateur complet et professionnel pour un langage\n"
            "d'expressions booléennes avec analyseur lexical, parser\n"
            "récursif descendant, AST, optimiseur et évaluateur."
        )
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)

        # Architecture
        arch_label = QLabel("Architecture:")
        arch_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        layout.addWidget(arch_label)

        arch_text = QLabel(
            "• Lexer (tokenizer) avec tracking ligne/colonne\n"
            "• Parser récursif descendant avec lookahead\n"
            "• AST extensible avec Visitor Pattern\n"
            "• Optimiseur avec constant folding\n"
            "• Évaluateur avec suggestions (Levenshtein)\n"
            "• Pretty-printer intelligent\n"
            "• Export Graphviz\n"
            "• Interface graphique PyQt6"
        )
        arch_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        arch_text.setStyleSheet("color: #CCCCCC; padding-left: 20px;")
        layout.addWidget(arch_text)

        # Auteur
        author = QLabel("Développé avec Python, PyQt6 et passion ❤️")
        author.setAlignment(Qt.AlignmentFlag.AlignCenter)
        author.setStyleSheet("color: #888888; font-style: italic; margin-top: 10px;")
        layout.addWidget(author)

        layout.addStretch()

        # Bouton Fermer
        close_btn = QPushButton("Fermer")
        close_btn.setMinimumHeight(35)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.setLayout(layout)

