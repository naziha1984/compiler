# Compilateur de Langage d'Expressions Logiques

Un compilateur complet et professionnel pour un langage d'expressions booléennes avec analyseur lexical, parser récursif descendant, AST, optimiseur, évaluateur et REPL interactive.

## 🎯 Fonctionnalités

### Core
- ✅ **Tokenizer robuste** avec tracking ligne/colonne et support des commentaires
- ✅ **Parser récursif descendant** avec lookahead et gestion d'erreurs avancée
- ✅ **AST extensible** avec Visitor Pattern, sérialisation JSON, comparaison d'égalité
- ✅ **Optimiseur** avec constant folding (NOT TRUE → FALSE, TRUE AND X → X, etc.)
- ✅ **Évaluateur** avec suggestions de variables (distance de Levenshtein)
- ✅ **Pretty-printer intelligent** avec minimisation de parenthèses
- ✅ **REPL interactive** avec commandes avancées et colorisation
- ✅ **Export Graphviz** pour visualiser l'AST
- ✅ **Application Desktop PyQt6** avec interface graphique complète

### Qualité de code
- ✅ Typage Python strict (mypy-friendly)
- ✅ Tests complets avec pytest
- ✅ Configuration Black, Ruff, pytest-cov
- ✅ Documentation intégrée
- ✅ Architecture modulaire et extensible

## 📦 Installation

```bash
# Cloner ou télécharger le projet
cd "PROJET COMPILER"

# Installer les dépendances
pip install -r requirements.txt

# Ou installer en mode développement
pip install -e ".[dev]"
```

**Note :** Pour l'interface graphique, PyQt6 est requis. Il sera installé automatiquement avec `requirements.txt`.

### Installation rapide de PyQt6

Si vous voulez uniquement l'interface graphique :

```bash
pip install PyQt6
```

## 🚀 Utilisation

### Application Desktop (PyQt6)

Lancez l'interface graphique complète :

```bash
python -m src.gui
```

L'application permet de :
- Saisir des expressions logiques avec **colorisation syntaxique**
- Visualiser les tokens, AST, JSON en temps réel
- **Auto-évaluation en temps réel** (option activable)
- **Drag & drop** de fichiers pour charger des expressions
- Évaluer des expressions avec un environnement personnalisé
- Optimiser des expressions
- Visualiser l'AST avec **Graphviz** (onglet dédié)
- **Thème dark mode** professionnel (Material Design)
- **Animations** fluides (fade-in, slide)
- Gérer les erreurs avec des messages clairs et surlignage

**Nouvelles fonctionnalités :**
- 🎨 **Thème Dark Mode** : Interface sombre moderne
- ⚡ **Auto-évaluation** : Menu Options → Évaluation en temps réel
- 📂 **Drag & Drop** : Glissez des fichiers `.txt`, `.expr`, `.logical`
- 🎞️ **Animations** : Transitions fluides entre les onglets
- 🌳 **Graphviz** : Visualisation graphique de l'AST
- 🎨 **Colorisation syntaxique** : Mots-clés, variables, parenthèses colorés
- ℹ️ **Fenêtre À propos** : Menu Aide → À propos

### REPL Interactive

```bash
python -m src.repl A=true B=false C=true
```

Dans la REPL, vous pouvez :

```python
# Évaluer des expressions
expr> A AND B
Résultat: False

expr> NOT (A OR B)
Résultat: False

# Utiliser les commandes
expr> :ast          # Afficher l'AST
expr> :tokens        # Afficher les tokens
expr> :opt           # Afficher l'AST optimisé
expr> :json          # Afficher l'AST en JSON
expr> :dot ast.dot   # Exporter en Graphviz
expr> :debug on      # Activer le mode debug
expr> :env D=true    # Modifier l'environnement
expr> :help          # Afficher l'aide
```

### Utilisation depuis Python

```python
from src import parse, evaluate, optimize
from src.pretty import pretty_print

# Parser une expression
expr = parse("A AND (B OR NOT C)")

# Évaluer
result = evaluate(expr, {"A": True, "B": False, "C": True})
print(result)  # True

# Optimiser
optimized = optimize(expr)
print(pretty_print(optimized))
```

### Export Graphviz

```python
from src import parse
from src.graphviz_exporter import export_to_dot

expr = parse("A AND (B OR C)")
export_to_dot(expr, "ast.dot")

# Puis visualiser avec:
# dot -Tpng ast.dot -o ast.png
```

## 📚 Grammaire

```text
expression  -> or ;
or          -> and ( OR and )* ;
and         -> not ( AND not )* ;
not         -> NOT not | primary ;
primary     -> IDENT | BOOL | '(' expression ')' ;
```

**Priorité des opérateurs :** `NOT > AND > OR`

**Identifiants :** `[A-Za-z_][A-Za-z0-9_]*`

**Mots-clés (insensibles à la casse) :** `AND`, `OR`, `NOT`, `TRUE`, `FALSE`

**Commentaires :** `# ...` (jusqu'à la fin de la ligne)

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Avec couverture de code
pytest --cov=src --cov-report=html

# Tests spécifiques
pytest tests/test_optimizer.py -v
```

## 🏗️ Architecture

```
/project
   /src
      errors.py              # Classes d'erreurs spécialisées
      tokenizer.py           # Analyseur lexical
      parser.py              # Parser récursif descendant
      ast.py                 # AST avec Visitor Pattern
      visitors.py            # Interface Visitor
      optimizer.py           # Optimiseur (constant folding)
      pretty.py              # Pretty-printer intelligent
      evaluator.py           # Évaluateur avec suggestions
      graphviz_exporter.py   # Export Graphviz
      repl.py                # REPL interactive
      gui.py                 # Application Desktop PyQt6
      style.qss              # Style pour l'interface graphique
   /tests
      test_tokenizer.py
      test_parser.py
      test_evaluator.py
      test_optimizer.py
      test_pretty.py
      test_json.py
      test_gui.py
   README.md
   requirements.txt
   pyproject.toml
```

## 🔧 Outils de développement

### Formatage et linting

```bash
# Formater le code avec Black
black src tests

# Linter avec Ruff
ruff check src tests

# Vérifier les types avec mypy
mypy src
```

### Pre-commit hooks

```bash
# Installer les hooks
pre-commit install

# Lancer manuellement
pre-commit run --all-files
```

## 📖 Exemples

### Exemples d'expressions

```python
# Expressions simples
"A AND B"
"A OR B"
"NOT A"

# Avec parenthèses
"(A OR B) AND C"
"NOT (A AND B)"

# Avec booléens littéraux
"TRUE AND FALSE"
"A OR TRUE"

# Commentaires
"A AND B  # commentaire"
```

### Optimisations

L'optimiseur applique automatiquement :

- `NOT TRUE` → `FALSE`
- `NOT FALSE` → `TRUE`
- `TRUE AND X` → `X`
- `FALSE AND X` → `FALSE`
- `TRUE OR X` → `TRUE`
- `FALSE OR X` → `X`
- `NOT NOT X` → `X`

### Gestion d'erreurs

Le compilateur fournit des messages d'erreur détaillés :

```python
# Erreur lexicale avec contexte
parse("A & B")
# LexicalError: Caractère inattendu '&' à la position 2
#   --> 1:3
# >>>    1 | A & B
#        |    ^

# Erreur de parsing avec suggestions
parse("A AND")
# MissingOperandError: Opérande manquant pour l'opérateur 'AND'

# Variable inconnue avec suggestions
evaluate(parse("UNKNON"), {"UNKNOWN": True})
# UnknownVariableError: Variable inconnue 'UNKNON'. Suggestions: UNKNOWN
```

## 🎨 Fonctionnalités avancées

### Pretty-printer avec options

```python
from src.pretty import pretty_print, CaseStyle

expr = parse("A AND B")

# Style de casse
pretty_print(expr, case_style=CaseStyle.UPPER)   # "A AND B"
pretty_print(expr, case_style=CaseStyle.LOWER)   # "a and b"
pretty_print(expr, case_style=CaseStyle.MIXED)    # "A And B"

# Parenthèses
pretty_print(expr, show_parentheses="minimal")    # Minimise
pretty_print(expr, show_parentheses="always")     # Toujours
pretty_print(expr, show_parentheses="never")      # Jamais
```

### Sérialisation JSON

```python
from src import parse
from src.ast import from_json
import json

expr = parse("A AND B")
json_data = expr.to_json()
# {"type": "And", "left": {"type": "Var", "name": "A"}, ...}

# Round-trip
restored = from_json(json_data)
assert restored == expr
```

### Mode debug

```python
import logging
logging.basicConfig(level=logging.DEBUG)

expr = parse("A AND B", debug=True)
# [ENTER] parse_expression
# [ENTER] parse_or
# [ENTER] parse_and
# ...

result = evaluate(expr, {"A": True, "B": False}, debug=True)
# [EVAL] AND
# [EVAL] Variable: A
# [EVAL] A = True
# ...
```

## 📝 Licence

MIT

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📧 Contact

Pour toute question, ouvrez une issue sur le dépôt.
