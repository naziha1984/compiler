
# Changelog - Version 2.0.0

## 🎉 Refonte complète du projet

Cette version apporte une refonte majeure avec de nombreuses améliorations et nouvelles fonctionnalités.

## ✨ Nouvelles fonctionnalités

### 1. Module d'erreurs centralisé (`errors.py`)
- Classes d'erreurs spécialisées : `UnexpectedTokenError`, `MissingParenthesisError`, `MissingOperandError`, `EndOfInputError`, `UnknownVariableError`
- Support du tracking ligne/colonne pour toutes les erreurs
- Formatage d'erreurs avec contexte (style GCC/Clang)

### 2. Tokenizer amélioré
- Tracking ligne/colonne pour chaque token
- Support des commentaires (`# ...`)
- Messages d'erreur contextuels avec affichage style GCC/Clang
- Mode debug pour afficher les tokens générés

### 3. Parser amélioré
- Support lookahead (`peek(k)`)
- Erreurs spécialisées avec messages contextuels
- Mode debug pour tracer les règles de parsing
- Messages d'erreur avec ligne/colonne

### 4. AST amélioré
- Visitor Pattern complet avec interface `ExprVisitor`
- Comparaison d'égalité (`__eq__`)
- Sérialisation JSON (`to_json()`, `from_json()`)
- Export Graphviz (via `graphviz_exporter.py`)

### 5. Optimiseur (`optimizer.py`)
- Constant folding avec règles :
  - `NOT TRUE` → `FALSE`
  - `NOT FALSE` → `TRUE`
  - `TRUE AND X` → `X`
  - `FALSE AND X` → `FALSE`
  - `TRUE OR X` → `TRUE`
  - `FALSE OR X` → `X`
  - `NOT NOT X` → `X`

### 6. Pretty-printer intelligent (`pretty.py`)
- Minimisation intelligente des parenthèses
- Respect de l'associativité et de la précédence
- Options de formatage (casse, parenthèses, indentation)

### 7. Évaluateur amélioré
- Suggestions de variables proches (distance de Levenshtein)
- Mode debug pour tracer l'évaluation
- Messages d'erreur détaillés

### 8. REPL améliorée
- Commandes avancées : `:ast`, `:tokens`, `:opt`, `:json`, `:dot`, `:debug`, `:env`, `:help`
- Colorisation de sortie (colorama)
- Support historique et auto-complétion (readline)

### 9. Export Graphviz (`graphviz_exporter.py`)
- Génération de fichiers `.dot` pour visualiser l'AST
- Support de la visualisation avec Graphviz

### 10. Tests améliorés
- Tests pour l'optimizer
- Tests pour le pretty-printer
- Tests pour les erreurs
- Tests pour la sérialisation JSON
- Tests de performance

### 11. Outils de développement
- `pyproject.toml` avec configuration Black, Ruff, pytest-cov
- Support pre-commit hooks
- Configuration mypy pour le typage

## 🔧 Améliorations techniques

- Architecture modulaire et extensible
- Typage Python strict (mypy-friendly)
- Documentation complète avec docstrings
- Code propre et maintenable
- Design patterns professionnels (Visitor Pattern)

## 📝 Migration depuis v1.0

Les principales différences :

1. **Imports** : Les erreurs sont maintenant dans `src.errors` au lieu d'être dans chaque module
2. **Tokens** : Les tokens ont maintenant `location` (ligne/colonne) au lieu de juste `position`
3. **AST** : Les nœuds AST ont maintenant `to_json()` et `from_json()`
4. **REPL** : Nouvelle interface avec commandes `:command`

## 🐛 Corrections de bugs

- Correction des tests de tokenizer
- Amélioration de la gestion d'erreurs
- Correction des imports circulaires

## 📚 Documentation

- README.md complet mis à jour
- Documentation intégrée dans tous les modules
- Exemples d'utilisation

