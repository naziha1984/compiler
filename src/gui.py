"""Application Desktop PyQt6 moderne pour le compilateur de langage logique.

Interface graphique professionnelle avec :
- Design moderne type Visual Studio Code / Material Dark
- Animations fluides et transitions
- Layouts responsive et adaptatifs
- Isolation complète des widgets
- Thème sombre cohérent
"""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path
from typing import Dict

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QTimer, Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsOpacityEffect,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from . import ast
from .about_dialog import AboutDialog
from .evaluator import evaluate
from .errors import CompilerError, LexicalError, ParseError
from .graphviz_widget import GraphvizWidget
from .optimizer import optimize
from .parser import parse
from .pretty import pretty_print as smart_pretty_print
from .syntax_highlighter import LogicalExpressionHighlighter
from .tokenizer import debug_tokens, tokenize

# Supprimer les warnings QSS
warnings.filterwarnings("ignore")


class AnimatedTabWidget(QTabWidget):
    """QTabWidget avec animations fluides lors du changement d'onglet."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.currentChanged.connect(self._animate_tab_change)

    def _animate_tab_change(self, index: int) -> None:
        """Anime le changement d'onglet avec un fade-in fluide.
        
        IMPORTANT: Ne modifie JAMAIS la visibilité du widget.
        """
        widget = self.widget(index)
        if widget is None:
            return

        try:
            opacity_effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(opacity_effect)

            animation = QPropertyAnimation(opacity_effect, b"opacity")
            animation.setStartValue(0.3)
            animation.setEndValue(1.0)
            animation.setDuration(200)
            animation.start()

            animation.finished.connect(lambda: widget.setGraphicsEffect(None))
        except Exception:
            widget.setGraphicsEffect(None)


class LogicalExpressionApp(QMainWindow):
    """Fenêtre principale de l'application de langage logique."""

    def __init__(self) -> None:
        super().__init__()
        self.current_expr: ast.Expr | None = None
        self.current_source: str = ""
        self.auto_eval_enabled = False
        self.auto_eval_timer = QTimer()
        self.auto_eval_timer.setSingleShot(True)
        self.auto_eval_timer.timeout.connect(self.on_evaluate_clicked)
        
        self._setup_ui()
        self._load_style()
        self._setup_drag_drop()

    def _setup_ui(self) -> None:
        """Initialise l'interface utilisateur."""
        self.setWindowTitle("Compilateur de Langage Logique")
        self.setGeometry(100, 100, 1600, 1000)
        self.setMinimumSize(1200, 700)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Barre de menu
        self._create_menu_bar()

        # Section de saisie
        input_group = self._create_input_section()
        main_layout.addWidget(input_group)

        # Section de résultats
        results_group = self._create_results_section()
        main_layout.addWidget(results_group, stretch=1)

        # Section d'erreurs
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        main_layout.addWidget(self.error_label)

    def _create_menu_bar(self) -> None:
        """Crée la barre de menu."""
        menubar = self.menuBar()

        # Menu Fichier
        file_menu = menubar.addMenu("Fichier")
        load_action = file_menu.addAction("Charger un fichier...")
        load_action.triggered.connect(self._load_file)
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Quitter")
        exit_action.triggered.connect(self.close)

        # Menu Options
        options_menu = menubar.addMenu("Options")
        auto_eval_action = options_menu.addAction("Évaluation en temps réel")
        auto_eval_action.setCheckable(True)
        auto_eval_action.triggered.connect(self._toggle_auto_eval)
        options_menu.addSeparator()
        dark_mode_action = options_menu.addAction("Mode sombre")
        dark_mode_action.setCheckable(True)
        dark_mode_action.setChecked(True)
        dark_mode_action.triggered.connect(lambda checked: self._load_style())

        # Menu Aide
        help_menu = menubar.addMenu("Aide")
        about_action = help_menu.addAction("À propos")
        about_action.triggered.connect(self._show_about)

    def _create_input_section(self) -> QGroupBox:
        """Crée la section de saisie."""
        group = QGroupBox("Saisie")
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Expression
        expr_label = QLabel("Expression logique:")
        expr_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.expression_input = QTextEdit()
        self.expression_input.setPlaceholderText("Ex: A AND (B OR NOT C)")
        self.expression_input.setFont(QFont("Consolas", 11))
        self.expression_input.setMaximumHeight(100)
        self.expression_input.textChanged.connect(self._on_expression_changed)
        self.highlighter = LogicalExpressionHighlighter(self.expression_input.document())

        # Environnement
        env_label = QLabel("Environnement (A=true,B=false,...):")
        env_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.environment_input = QLineEdit()
        self.environment_input.setPlaceholderText("A=true,B=false,C=true")
        self.environment_input.setFont(QFont("Consolas", 11))
        self.environment_input.setText("A=true,B=false,C=true")
        self.environment_input.textChanged.connect(self._on_env_changed)

        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.evaluate_btn = QPushButton("Évaluer")
        self.evaluate_btn.setObjectName("evaluateBtn")
        self.evaluate_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.evaluate_btn.setMinimumHeight(42)
        self.evaluate_btn.clicked.connect(self.on_evaluate_clicked)

        self.optimize_btn = QPushButton("Optimiser")
        self.optimize_btn.setObjectName("optimizeBtn")
        self.optimize_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.optimize_btn.setMinimumHeight(42)
        self.optimize_btn.clicked.connect(self.on_optimize_clicked)

        buttons_layout.addWidget(self.evaluate_btn)
        buttons_layout.addWidget(self.optimize_btn)
        buttons_layout.addStretch()

        layout.addWidget(expr_label)
        layout.addWidget(self.expression_input)
        layout.addWidget(env_label)
        layout.addWidget(self.environment_input)
        layout.addLayout(buttons_layout)

        group.setLayout(layout)
        return group

    def _create_results_section(self) -> QGroupBox:
        """Crée la section de résultats avec onglets isolés.
        
        Chaque onglet utilise un container QWidget dédié pour garantir
        l'isolation complète des widgets.
        """
        group = QGroupBox("Résultats")
        layout = QVBoxLayout()
        layout.setSpacing(0)

        # Onglets avec animation
        self.tabs = AnimatedTabWidget()
        self.tabs.setFont(QFont("Segoe UI", 10))

        # Onglet 0: Tokens
        tokens_container = self._create_tab_container("tokensContainer")
        self.tokens_text = self._create_text_edit("tokensText", font_size=10)
        tokens_container.layout().addWidget(self.tokens_text)
        self.tabs.addTab(tokens_container, "Tokens")

        # Onglet 1: AST
        ast_container = self._create_tab_container("astContainer")
        self.ast_text = self._create_text_edit("astText", font_size=10)
        ast_container.layout().addWidget(self.ast_text)
        self.tabs.addTab(ast_container, "AST")

        # Onglet 2: Pretty-Printer
        pretty_container = self._create_tab_container("prettyContainer")
        self.pretty_text = self._create_text_edit("prettyText", font_size=11)
        pretty_container.layout().addWidget(self.pretty_text)
        self.tabs.addTab(pretty_container, "Pretty-Printer")

        # Onglet 3: AST Optimisé
        optimized_container = self._create_tab_container("optimizedContainer")
        self.optimized_text = self._create_text_edit("optimizedText", font_size=10)
        optimized_container.layout().addWidget(self.optimized_text)
        self.tabs.addTab(optimized_container, "AST Optimisé")

        # Onglet 4: JSON
        json_container = self._create_tab_container("jsonContainer")
        self.json_text = self._create_text_edit("jsonText", font_size=10)
        json_container.layout().addWidget(self.json_text)
        self.tabs.addTab(json_container, "JSON")

        # Onglet 5: Graphviz
        self.graphviz_widget = GraphvizWidget()
        self.graphviz_widget.setObjectName("graphvizWidget")
        self.tabs.addTab(self.graphviz_widget, "Graphviz")

        # Vérification d'isolation
        self._verify_widget_isolation()

        layout.addWidget(self.tabs)
        group.setLayout(layout)
        return group

    def _create_tab_container(self, object_name: str) -> QWidget:
        """Crée un container pour un onglet."""
        container = QWidget()
        container.setObjectName(object_name)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        return container

    def _create_text_edit(self, object_name: str, font_size: int = 10) -> QTextEdit:
        """Crée un QTextEdit configuré."""
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setFont(QFont("Consolas", font_size))
        text_edit.setObjectName(object_name)
        text_edit.setVisible(True)
        text_edit.setMinimumHeight(200)
        return text_edit

    def _verify_widget_isolation(self) -> None:
        """Vérifie que tous les widgets sont isolés."""
        all_widgets = [
            self.tokens_text,
            self.ast_text,
            self.pretty_text,
            self.optimized_text,
            self.json_text,
            self.graphviz_widget,
        ]
        widget_ids = [id(w) for w in all_widgets]
        if len(widget_ids) != len(set(widget_ids)):
            raise ValueError("Des widgets sont partagés entre plusieurs onglets!")

    def _setup_drag_drop(self) -> None:
        """Configure le drag & drop."""
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Gère l'entrée d'un drag."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        """Gère le drop d'un fichier."""
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            file_path = Path(url.toLocalFile())
            if file_path.suffix in [".txt", ".expr", ".logical"]:
                try:
                    content = file_path.read_text(encoding="utf-8").strip()
                    self.expression_input.setPlainText(content)
                    if self.auto_eval_enabled:
                        self.on_evaluate_clicked()
                except Exception as e:
                    self.show_error(f"Erreur lors du chargement: {e}")

    def _load_style(self) -> None:
        """Charge le fichier de style QSS."""
        style_path = Path(__file__).parent / "style.qss"
        if style_path.exists():
            try:
                with open(style_path, "r", encoding="utf-8") as f:
                    self.setStyleSheet(f.read())
            except Exception:
                pass

    def _load_file(self) -> None:
        """Charge un fichier depuis le menu."""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Charger une expression",
            "",
            "Fichiers texte (*.txt *.expr *.logical);;Tous les fichiers (*)",
        )
        if filename:
            try:
                content = Path(filename).read_text(encoding="utf-8").strip()
                self.expression_input.setPlainText(content)
                if self.auto_eval_enabled:
                    self.on_evaluate_clicked()
            except Exception as e:
                self.show_error(f"Erreur lors du chargement: {e}")

    def _toggle_auto_eval(self, enabled: bool) -> None:
        """Active/désactive l'auto-évaluation."""
        self.auto_eval_enabled = enabled

    def _show_about(self) -> None:
        """Affiche la fenêtre À propos."""
        dialog = AboutDialog(self)
        dialog.exec()

    def _on_expression_changed(self) -> None:
        """Appelé quand l'expression change."""
        self.error_label.hide()
        self.current_source = self.expression_input.toPlainText()
        if self.auto_eval_enabled:
            self.auto_eval_timer.stop()
            self.auto_eval_timer.start(500)

    def _on_env_changed(self) -> None:
        """Appelé quand l'environnement change."""
        if self.auto_eval_enabled and self.current_expr:
            self.auto_eval_timer.stop()
            self.auto_eval_timer.start(300)

    def _animate_fade_in(self, widget: QWidget) -> None:
        """Anime un widget avec un fade-in fluide (opacité uniquement).
        
        IMPORTANT: Ne modifie JAMAIS la visibilité du widget.
        """
        try:
            opacity_effect = QGraphicsOpacityEffect(widget)
            widget.setGraphicsEffect(opacity_effect)

            animation = QPropertyAnimation(opacity_effect, b"opacity")
            animation.setStartValue(0.3)
            animation.setEndValue(1.0)
            animation.setDuration(200)
            animation.start()

            animation.finished.connect(lambda: widget.setGraphicsEffect(None))
        except Exception:
            widget.setGraphicsEffect(None)

    def _update_widget_content(self, widget: QTextEdit, content: str) -> None:
        """Met à jour le contenu d'un widget de manière isolée.
        
        Version simplifiée : juste setPlainText() + repaint().
        Ne modifie JAMAIS la visibilité.
        """
        if widget is None:
            return
        
        # Vérification d'isolation
        assert widget.objectName() in ["tokensText", "astText", "prettyText", "optimizedText", "jsonText"], \
            f"Widget {widget.objectName()} non autorisé!"
        
        # Mettre le texte et forcer le rafraîchissement
        widget.setPlainText(content)
        widget.repaint()

    def update_tokens_tab(self, source: str) -> None:
        """Met à jour l'onglet Tokens."""
        if self.tokens_text is None:
            return

        try:
            tokens = tokenize(source)
            tokens_str = debug_tokens(tokens)
            self._update_widget_content(self.tokens_text, tokens_str)
        except Exception as e:
            if self.tokens_text is not None:
                self._update_widget_content(self.tokens_text, f"Erreur: {e}")

    def update_ast_tab(self, expr: ast.Expr) -> None:
        """Met à jour l'onglet AST."""
        if self.ast_text is None:
            return

        try:
            ast_str = ast.pretty_print(expr)
            self._update_widget_content(self.ast_text, ast_str)
        except Exception as e:
            if self.ast_text is not None:
                self._update_widget_content(self.ast_text, f"Erreur: {e}")

    def update_pretty_tab(self, expr: ast.Expr, show_result: bool = True) -> None:
        """Met à jour l'onglet Pretty-Printer."""
        if self.pretty_text is None:
            return

        try:
            pretty_str = smart_pretty_print(expr)
            if show_result:
                env_str = self.environment_input.text()
                env = self.parse_environment(env_str)
                try:
                    result = evaluate(expr, env)
                    pretty_str = f"Résultat: {result}\n\nExpression: {pretty_str}\n\nEnvironnement: {env}"
                except Exception as e:
                    pretty_str = f"Expression: {pretty_str}\n\nErreur d'évaluation: {e}"

            self._update_widget_content(self.pretty_text, pretty_str)
        except Exception as e:
            if self.pretty_text is not None:
                self._update_widget_content(self.pretty_text, f"Erreur: {e}")

    def update_optimized_ast_tab(self, expr: ast.Expr) -> None:
        """Met à jour l'onglet AST Optimisé."""
        if self.optimized_text is None:
            return

        try:
            ast_str = ast.pretty_print(expr)
            self._update_widget_content(self.optimized_text, ast_str)
        except Exception as e:
            if self.optimized_text is not None:
                self._update_widget_content(self.optimized_text, f"Erreur: {e}")

    def update_json_tab(self, expr: ast.Expr) -> None:
        """Met à jour l'onglet JSON."""
        if self.json_text is None:
            return

        try:
            json_data = expr.to_json()
            json_str = json.dumps(json_data, indent=2, ensure_ascii=False)
            self._update_widget_content(self.json_text, json_str)
        except Exception as e:
            if self.json_text is not None:
                self._update_widget_content(self.json_text, f"Erreur: {e}")

    def update_graphviz_tab(self, expr: ast.Expr) -> None:
        """Met à jour l'onglet Graphviz."""
        if self.graphviz_widget is None:
            return

        try:
            self.graphviz_widget.update_graph(expr)
        except Exception:
            pass

    def on_evaluate_clicked(self) -> None:
        """Évalue l'expression et met à jour tous les onglets."""
        self.error_label.hide()
        source = self.expression_input.toPlainText().strip()

        if not source:
            self.show_error("Veuillez saisir une expression.")
            return

        try:
            # Parser (doit être fait en premier pour avoir expr)
            expr = parse(source)
            self.current_expr = expr
            self.current_source = source

            # Mettre à jour tous les onglets via les méthodes centralisées
            self.update_tokens_tab(source)
            self.update_ast_tab(expr)
            self.update_optimized_ast_tab(expr)
            self.update_pretty_tab(expr, show_result=True)
            self.update_json_tab(expr)
            self.update_graphviz_tab(expr)

        except LexicalError as e:
            self.show_compiler_error(e, "Erreur lexicale")
            if hasattr(e, "location") and e.location:
                try:
                    self.highlighter.highlight_error(e.location.offset, 1)
                except Exception:
                    pass
        except ParseError as e:
            self.show_compiler_error(e, "Erreur de parsing")
            if hasattr(e, "location") and e.location:
                try:
                    self.highlighter.highlight_error(e.location.offset, 1)
                except Exception:
                    pass
        except Exception as e:
            self.show_error(f"Erreur inattendue: {e}")

    def on_optimize_clicked(self) -> None:
        """Optimise l'expression et met à jour les onglets."""
        self.error_label.hide()
        source = self.expression_input.toPlainText().strip()

        if not source:
            self.show_error("Veuillez saisir une expression.")
            return

        try:
            # Parser
            expr = parse(source)
            self.current_expr = expr

            # Optimiser
            optimized_expr = optimize(expr, debug=False)

            # Mettre à jour tous les onglets avec l'expression optimisée
            self.update_tokens_tab(source)
            self.update_ast_tab(expr)  # AST original
            self.update_optimized_ast_tab(optimized_expr)
            
            # Pretty-print avec comparaison
            optimized_pretty = smart_pretty_print(optimized_expr)
            original_pretty = smart_pretty_print(expr)
            pretty_output = f"Expression originale:\n{original_pretty}\n\nExpression optimisée:\n{optimized_pretty}"
            if self.pretty_text is not None:
                self._update_widget_content(self.pretty_text, pretty_output)

            # JSON optimisé
            self.update_json_tab(optimized_expr)

            # Graphviz optimisé
            self.update_graphviz_tab(optimized_expr)

            # Passer à l'onglet optimisé
            self.tabs.setCurrentIndex(3)

        except LexicalError as e:
            self.show_compiler_error(e, "Erreur lexicale")
        except ParseError as e:
            self.show_compiler_error(e, "Erreur de parsing")
        except Exception as e:
            self.show_error(f"Erreur inattendue: {e}")

    def parse_environment(self, env_str: str) -> Dict[str, bool]:
        """Parse une chaîne d'environnement en dictionnaire."""
        env: Dict[str, bool] = {}
        if not env_str.strip():
            return env

        for pair in env_str.split(","):
            pair = pair.strip()
            if "=" in pair:
                key, value = pair.split("=", 1)
                key = key.strip()
                value = value.strip().lower()
                env[key] = value in ("true", "1", "yes", "on")

        return env

    def show_compiler_error(self, error: CompilerError, title: str) -> None:
        """Affiche une erreur du compilateur."""
        error_msg = str(error)
        if hasattr(error, "format_error"):
            try:
                error_msg = error.format_error()
            except Exception:
                pass

        self.error_label.setText(f"❌ {title}: {error_msg}")
        self.error_label.show()

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(error_msg)
        if hasattr(error, "__str__"):
            msg_box.setDetailedText(str(error))
        msg_box.exec()

        # Vider les onglets en cas d'erreur
        self._clear_all_tabs()

    def show_error(self, message: str) -> None:
        """Affiche une erreur simple."""
        self.error_label.setText(f"❌ {message}")
        self.error_label.show()

        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Erreur")
        msg_box.setText(message)
        msg_box.exec()

    def _clear_all_tabs(self) -> None:
        """Vide tous les onglets."""
        widgets = [self.tokens_text, self.ast_text, self.pretty_text, 
                   self.optimized_text, self.json_text]
        for widget in widgets:
            if widget is not None:
                widget.clear()
                widget.setPlainText("")


def main() -> None:
    """Point d'entrée principal de l'application."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Supprimer les warnings
    warnings.filterwarnings("ignore")
    import logging
    logging.getLogger().setLevel(logging.ERROR)

    window = LogicalExpressionApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
