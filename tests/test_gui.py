"""Tests pour l'interface graphique PyQt6.

Ces tests vérifient que le module GUI peut être importé et que
les composants de base fonctionnent correctement.
"""

import pytest

# Vérifier que PyQt6 est disponible
try:
    from PyQt6.QtWidgets import QApplication
    PYQT6_AVAILABLE = True
except ImportError:
    PYQT6_AVAILABLE = False

pytestmark = pytest.mark.skipif(not PYQT6_AVAILABLE, reason="PyQt6 n'est pas installé")


def test_gui_import():
    """Test que le module GUI peut être importé."""
    from src import gui

    assert hasattr(gui, "LogicalExpressionApp")
    assert hasattr(gui, "main")


def test_gui_app_creation():
    """Test que l'application peut être créée."""
    from PyQt6.QtWidgets import QApplication
    from src.gui import LogicalExpressionApp

    # Créer une application Qt (nécessaire pour créer des widgets)
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    # Créer la fenêtre principale
    window = LogicalExpressionApp()

    assert window is not None
    assert window.windowTitle() == "Compilateur de Langage Logique"

    # Vérifier que les composants existent
    assert hasattr(window, "expression_input")
    assert hasattr(window, "environment_input")
    assert hasattr(window, "evaluate_btn")
    assert hasattr(window, "optimize_btn")
    assert hasattr(window, "tabs")


def test_parse_environment():
    """Test la fonction de parsing d'environnement."""
    from PyQt6.QtWidgets import QApplication
    from src.gui import LogicalExpressionApp

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    window = LogicalExpressionApp()

    # Test parsing simple
    env = window.parse_environment("A=true,B=false")
    assert env == {"A": True, "B": False}

    # Test avec espaces
    env = window.parse_environment("A=true, B=false, C=true")
    assert env == {"A": True, "B": False, "C": True}

    # Test vide
    env = window.parse_environment("")
    assert env == {}

    # Test valeurs alternatives
    env = window.parse_environment("A=1,B=0,C=yes,D=no")
    assert env == {"A": True, "B": False, "C": True, "D": False}


def test_gui_components_exist():
    """Test que tous les composants de l'interface existent."""
    from PyQt6.QtWidgets import QApplication
    from src.gui import LogicalExpressionApp

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    window = LogicalExpressionApp()

    # Vérifier les champs de saisie
    assert window.expression_input is not None
    assert window.environment_input is not None

    # Vérifier les boutons
    assert window.evaluate_btn is not None
    assert window.optimize_btn is not None

    # Vérifier les onglets
    assert window.tabs is not None
    assert window.tabs.count() == 6  # Tokens, AST, Pretty-Printer, Optimized AST, JSON, Graphviz

    # Vérifier les zones de texte
    assert window.tokens_text is not None
    assert window.ast_text is not None
    assert window.pretty_text is not None
    assert window.optimized_text is not None
    assert window.json_text is not None

