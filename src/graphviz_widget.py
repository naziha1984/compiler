"""Widget moderne pour afficher les graphiques Graphviz dans l'application."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from . import ast
from .graphviz_exporter import export_to_dot


class GraphvizWidget(QWidget):
    """Widget moderne pour afficher et exporter des graphiques Graphviz."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.current_expr: ast.Expr | None = None
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialise l'interface du widget."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Label pour l'image
        self.image_label = QLabel()
        self.image_label.setObjectName("graphvizImageLabel")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setText(
            "Aucun graphique disponible.\nGénérez une expression pour voir l'AST."
        )
        self.image_label.setWordWrap(True)
        self.image_label.setScaledContents(False)
        layout.addWidget(self.image_label, stretch=1)

        # Bouton d'export
        self.export_btn = QPushButton("Exporter Graphviz (PNG)")
        self.export_btn.setMinimumHeight(40)
        self.export_btn.clicked.connect(self._export_png)
        self.export_btn.setEnabled(False)
        layout.addWidget(self.export_btn)

    def update_graph(self, expr: ast.Expr) -> None:
        """Met à jour le graphique avec une nouvelle expression.
        
        Écrit UNIQUEMENT dans self.image_label.
        IMPORTANT: Ne supprime JAMAIS les fichiers avant que QPixmap les ait chargés.
        """
        self.current_expr = expr
        
        dot_path = None
        png_path = None
        
        try:
            # Générer le fichier DOT
            with tempfile.NamedTemporaryFile(mode="w", suffix=".dot", delete=False, encoding="utf-8") as f:
                dot_path = f.name
                export_to_dot(expr, dot_path)

            # Générer le PNG
            png_path = dot_path.replace(".dot", ".png")
            try:
                result = subprocess.run(
                    ["dot", "-Tpng", dot_path, "-o", png_path],
                    check=True,
                    capture_output=True,
                    timeout=10,
                )

                # Vérifier que le fichier PNG existe et n'est pas vide
                if not Path(png_path).exists() or Path(png_path).stat().st_size == 0:
                    raise ValueError("Le fichier PNG généré est vide ou n'existe pas")

                # CRITIQUE: Charger l'image COMPLÈTEMENT AVANT de supprimer les fichiers
                # QPixmap doit avoir le fichier disponible pendant TOUT le chargement
                pixmap = QPixmap()
                
                # Charger depuis le fichier
                if not pixmap.load(png_path):
                    raise ValueError("Impossible de charger le fichier PNG")
                
                # Vérifier que le pixmap est valide
                if pixmap.isNull():
                    raise ValueError("Le pixmap chargé est null")
                
                # Redimensionner si trop grand
                if pixmap.width() > 1000 or pixmap.height() > 800:
                    pixmap = pixmap.scaled(
                        1000, 800,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )

                # Afficher l'image (le pixmap est maintenant complètement chargé en mémoire)
                self.image_label.clear()
                self.image_label.setPixmap(pixmap)
                self.image_label.setText("")
                self.image_label.repaint()
                self.export_btn.setEnabled(True)
                
                # MAINTENANT on peut supprimer les fichiers (le pixmap est complètement chargé en mémoire)
                if dot_path and Path(dot_path).exists():
                    Path(dot_path).unlink(missing_ok=True)
                if png_path and Path(png_path).exists():
                    Path(png_path).unlink(missing_ok=True)
                dot_path = None
                png_path = None
            except FileNotFoundError:
                error_msg = (
                    "Graphviz n'est pas installé.\n\n"
                    "Installez Graphviz pour visualiser les AST:\n"
                    "https://graphviz.org/download/"
                )
                self.image_label.clear()
                self.image_label.setPixmap(QPixmap())
                self.image_label.setText(error_msg)
                self.image_label.repaint()
                self.export_btn.setEnabled(False)
            except FileNotFoundError:
                error_msg = (
                    "Graphviz n'est pas installé.\n\n"
                    "Installez Graphviz pour visualiser les AST:\n"
                    "https://graphviz.org/download/"
                )
                self.image_label.clear()
                self.image_label.setPixmap(QPixmap())
                self.image_label.setText(error_msg)
                self.image_label.repaint()
                self.export_btn.setEnabled(False)
            except subprocess.TimeoutExpired:
                error_msg = "Timeout: La génération du graphique a pris trop de temps."
                self.image_label.clear()
                self.image_label.setPixmap(QPixmap())
                self.image_label.setText(error_msg)
                self.image_label.repaint()
                self.export_btn.setEnabled(False)
            except subprocess.CalledProcessError as e:
                error_msg = "Erreur lors de la génération du graphique"
                try:
                    if e.stderr:
                        stderr_text = e.stderr.decode('utf-8', errors='ignore')
                        error_msg += f":\n{stderr_text[:200]}"
                except Exception:
                    pass
                self.image_label.clear()
                self.image_label.setPixmap(QPixmap())
                self.image_label.setText(error_msg)
                self.image_label.repaint()
                self.export_btn.setEnabled(False)
            except Exception as e:
                error_msg = f"Erreur inattendue: {str(e)[:200]}"
                self.image_label.clear()
                self.image_label.setPixmap(QPixmap())
                self.image_label.setText(error_msg)
                self.image_label.repaint()
                self.export_btn.setEnabled(False)
        except Exception as e:
            error_msg = f"Erreur lors de l'export DOT: {str(e)[:200]}"
            self.image_label.clear()
            self.image_label.setPixmap(QPixmap())
            self.image_label.setText(error_msg)
            self.export_btn.setEnabled(False)
        finally:
            # Nettoyer les fichiers temporaires s'ils existent encore (seulement si pas déjà supprimés)
            if dot_path and Path(dot_path).exists():
                Path(dot_path).unlink(missing_ok=True)
            if png_path and Path(png_path).exists():
                Path(png_path).unlink(missing_ok=True)

    def _export_png(self) -> None:
        """Exporte le graphique actuel en PNG."""
        if self.current_expr is None:
            return

        from PyQt6.QtWidgets import QFileDialog, QMessageBox

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter Graphviz",
            "ast.png",
            "Images PNG (*.png);;Tous les fichiers (*)",
        )

        if filename:
            try:
                with tempfile.NamedTemporaryFile(mode="w", suffix=".dot", delete=False, encoding="utf-8") as f:
                    dot_path = f.name
                    export_to_dot(self.current_expr, dot_path)

                subprocess.run(
                    ["dot", "-Tpng", dot_path, "-o", filename],
                    check=True,
                    capture_output=True,
                )

                Path(dot_path).unlink(missing_ok=True)

                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Export réussi")
                msg.setText(f"Graphique exporté vers:\n{filename}")
                msg.exec()

            except Exception as e:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("Erreur d'export")
                msg.setText(f"Erreur lors de l'export:\n{e}")
                msg.exec()
