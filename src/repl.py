"""REPL (Read-Eval-Print Loop) améliorée pour le langage logique.

Ce module implémente une REPL interactive avec :
- Commandes avancées (:ast, :tokens, :opt, :json, :dot, :debug, :env, :help)
- Colorisation de sortie (colorama)
- Historique et auto-complétion (readline)
- Mode debug
"""

from __future__ import annotations

import json
import logging
import sys
from io import StringIO
from typing import Dict

try:
    import readline  # noqa: F401 - pour l'historique et auto-complétion
except ImportError:
    pass  # readline n'est pas disponible sur Windows par défaut

try:
    from colorama import Fore, Style, init

    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    # Fallback si colorama n'est pas installé
    class Fore:
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        CYAN = ""
        MAGENTA = ""

    class Style:
        RESET_ALL = ""
        BRIGHT = ""

    HAS_COLORAMA = False

from . import ast
from .evaluator import evaluate
from .optimizer import optimize
from .parser import parse
from .pretty import pretty_print as smart_pretty_print
from .tokenizer import debug_tokens, tokenize
from .graphviz_exporter import export_to_dot

logger = logging.getLogger(__name__)


def _colorize(text: str, color: str) -> str:
    """Colorise un texte si colorama est disponible."""
    if HAS_COLORAMA:
        return f"{color}{text}{Style.RESET_ALL}"
    return text


def _print_banner() -> None:
    """Affiche la bannière de bienvenue."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║   REPL - Langage d'expressions logiques (AND, OR, NOT)     ║
║   Priorité: NOT > AND > OR                                  ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(_colorize(banner, Fore.CYAN))
    print(_colorize("Tapez une expression ou ':help' pour voir les commandes.\n", Fore.YELLOW))


def _parse_env(args: list[str]) -> Dict[str, bool]:
    """Parse les variables passées sur la ligne de commande.

    Format attendu : A=true B=false ... ou A=true,B=false
    """
    env: Dict[str, bool] = {}
    for arg in args:
        # Support des deux formats : "A=true B=false" et "A=true,B=false"
        pairs = arg.split(",") if "," in arg else [arg]
        for pair in pairs:
            if "=" not in pair:
                continue
            name, value = pair.split("=", 1)
            name = name.strip()
            v = value.strip().lower()
            if v in ("true", "1", "yes", "on"):
                env[name] = True
            elif v in ("false", "0", "no", "off"):
                env[name] = False
            else:
                print(
                    _colorize(
                        f"Valeur invalide pour {name}: {value!r} (utiliser true/false)",
                        Fore.RED,
                    ),
                    file=sys.stderr,
                )
    return env


class REPL:
    """REPL interactive avec commandes avancées."""

    def __init__(self, initial_env: Dict[str, bool] | None = None) -> None:
        """Initialise la REPL.

        Args:
            initial_env: Environnement initial de variables
        """
        self.env: Dict[str, bool] = dict(initial_env or {})
        self.debug = False
        self.last_expr: ast.Expr | None = None
        self.last_source: str = ""

    def _print_help(self) -> None:
        """Affiche l'aide des commandes."""
        help_text = """
Commandes disponibles:

  :ast      Afficher l'AST formaté de la dernière expression
  :tokens   Afficher les tokens de la dernière expression
  :opt      Afficher l'AST optimisé de la dernière expression
  :json     Afficher l'AST en format JSON
  :dot      Exporter l'AST en format Graphviz DOT
  :debug    Activer/désactiver le mode debug (on/off)
  :env      Afficher ou modifier l'environnement (A=true,B=false)
  :help     Afficher cette aide
  :quit     Quitter la REPL

Exemples:
  A AND B
  NOT (A OR B)
  :env A=true,B=false,C=true
  :debug on
"""
        print(_colorize(help_text, Fore.CYAN))

    def _handle_command(self, line: str) -> bool:
        """Gère une commande REPL. Retourne True si la commande a été traitée."""
        line = line.strip()
        if not line.startswith(":"):
            return False

        cmd = line[1:].strip().lower()
        parts = cmd.split(None, 1)
        cmd_name = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        if cmd_name == "help":
            self._print_help()
        elif cmd_name == "quit" or cmd_name == "exit":
            return True  # Signal pour quitter
        elif cmd_name == "ast":
            if self.last_expr:
                print(_colorize("AST:", Fore.BLUE))
                print(ast.pretty_print(self.last_expr))
            else:
                print(_colorize("Aucune expression précédente.", Fore.YELLOW))
        elif cmd_name == "tokens":
            if self.last_source:
                try:
                    tokens = tokenize(self.last_source)
                    print(_colorize("Tokens:", Fore.BLUE))
                    print(debug_tokens(tokens))
                except Exception as e:
                    print(_colorize(f"Erreur: {e}", Fore.RED))
            else:
                print(_colorize("Aucune expression précédente.", Fore.YELLOW))
        elif cmd_name == "opt":
            if self.last_expr:
                optimized = optimize(self.last_expr, debug=self.debug)
                print(_colorize("AST optimisé:", Fore.BLUE))
                print(ast.pretty_print(optimized))
                print(_colorize("Expression optimisée:", Fore.GREEN))
                print(smart_pretty_print(optimized))
            else:
                print(_colorize("Aucune expression précédente.", Fore.YELLOW))
        elif cmd_name == "json":
            if self.last_expr:
                json_str = json.dumps(self.last_expr.to_json(), indent=2)
                print(_colorize("AST JSON:", Fore.BLUE))
                print(json_str)
            else:
                print(_colorize("Aucune expression précédente.", Fore.YELLOW))
        elif cmd_name == "dot":
            if self.last_expr:
                filename = args.strip() if args else "ast.dot"
                try:
                    export_to_dot(self.last_expr, filename)
                    print(_colorize(f"AST exporté vers {filename}", Fore.GREEN))
                except Exception as e:
                    print(_colorize(f"Erreur: {e}", Fore.RED))
            else:
                print(_colorize("Aucune expression précédente.", Fore.YELLOW))
        elif cmd_name == "debug":
            if args.lower() in ("on", "true", "1", "yes"):
                self.debug = True
                logging.basicConfig(level=logging.DEBUG)
                print(_colorize("Mode debug activé", Fore.GREEN))
            elif args.lower() in ("off", "false", "0", "no"):
                self.debug = False
                logging.basicConfig(level=logging.WARNING)
                print(_colorize("Mode debug désactivé", Fore.YELLOW))
            else:
                status = "activé" if self.debug else "désactivé"
                print(_colorize(f"Mode debug: {status}", Fore.CYAN))
        elif cmd_name == "env":
            if args:
                # Modifier l'environnement
                new_env = _parse_env([args])
                self.env.update(new_env)
                print(_colorize(f"Environnement mis à jour: {self.env}", Fore.GREEN))
            else:
                # Afficher l'environnement
                print(_colorize(f"Environnement: {self.env}", Fore.CYAN))
        else:
            print(_colorize(f"Commande inconnue: :{cmd_name}. Tapez :help pour l'aide.", Fore.RED))

        return False  # Ne pas quitter

    def run(self) -> None:
        """Lance la boucle REPL."""
        _print_banner()
        print(_colorize(f"Environnement initial: {self.env}\n", Fore.CYAN))

        while True:
            try:
                line = input(_colorize("expr> ", Fore.GREEN)).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not line:
                continue

            # Gérer les commandes
            if line.startswith(":"):
                should_quit = self._handle_command(line)
                if should_quit:
                    break
                continue

            # Parser et évaluer l'expression
            self.last_source = line
            try:
                expr = parse(line, debug=self.debug)
                self.last_expr = expr
            except Exception as e:
                print(_colorize(f"[Erreur de parsing] {e}", Fore.RED))
                if hasattr(e, "format_error"):
                    print(e.format_error())
                continue

            # Afficher l'AST si demandé (ou en mode debug)
            if self.debug:
                print(_colorize("AST:", Fore.BLUE))
                print(ast.pretty_print(expr))

            # Évaluer
            try:
                result = evaluate(expr, self.env, debug=self.debug)
                print(_colorize(f"Résultat: {result}", Fore.GREEN))
            except Exception as e:
                print(_colorize(f"[Erreur d'évaluation] {e}", Fore.RED))
                continue

            print()  # Ligne vide pour la lisibilité


def repl(initial_env: Dict[str, bool] | None = None) -> None:
    """Fonction utilitaire pour lancer la REPL.

    Args:
        initial_env: Environnement initial de variables
    """
    repl_instance = REPL(initial_env)
    repl_instance.run()


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée principal de la REPL."""
    if argv is None:
        argv = sys.argv[1:]
    env = _parse_env(argv)
    repl(env)
    return 0


if __name__ == "__main__":  # pragma: no cover - point d'entrée CLI
    raise SystemExit(main())
