# 🚀 Guide d'Exécution du Projet

## ✅ Dépendances installées

Toutes les dépendances sont déjà installées :
- ✅ Python 3.13.5
- ✅ PyQt6 (pour l'interface graphique)
- ✅ PLY (pour Flex/Bison)
- ✅ Toutes les autres dépendances

## 🎯 Méthodes d'exécution

### 1. Application GUI (Interface Graphique) - ⭐ RECOMMANDÉ

L'application graphique moderne avec thème dark mode.

#### Méthode 1 : Script PowerShell
```powershell
.\launch_gui.ps1
```

#### Méthode 2 : Script Batch
```cmd
launch_gui.bat
```

#### Méthode 3 : Commande Python directe
```powershell
python -m src.gui
```

**Fonctionnalités de l'application :**
- 🎨 Interface moderne avec thème dark mode
- ✨ Colorisation syntaxique en temps réel
- 📊 Visualisation des tokens, AST, JSON
- 🌳 Visualisation Graphviz de l'AST
- ⚡ Auto-évaluation en temps réel
- 📂 Drag & Drop de fichiers

### 2. REPL Interactif (Ligne de commande)

Interface en ligne de commande pour tester rapidement.

#### Méthode 1 : Script PowerShell
```powershell
.\run.ps1
```

#### Méthode 2 : Script Batch
```cmd
run.bat
```

#### Méthode 3 : Commande Python directe
```powershell
python -m src.repl A=true B=false C=true
```

**Commandes disponibles dans le REPL :**
```
expr> A AND B                    # Évaluer une expression
expr> :ast                       # Afficher l'AST
expr> :tokens                    # Afficher les tokens
expr> :opt                       # Afficher l'AST optimisé
expr> :json                      # Afficher l'AST en JSON
expr> :dot ast.dot               # Exporter en Graphviz
expr> :env D=true                # Modifier l'environnement
expr> :debug on                  # Activer le mode debug
expr> :help                      # Afficher l'aide
expr> quit                       # Quitter
```

### 3. Utilisation depuis Python

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

### 4. Tests

Lancer tous les tests :
```powershell
pytest
```

Avec couverture de code :
```powershell
pytest --cov=src --cov-report=html
```

## 📝 Exemples d'expressions

Vous pouvez tester ces expressions dans l'application ou le REPL :

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

# Avec commentaires
"A AND B  # commentaire"
```

## 🐛 Dépannage

### L'application GUI ne se lance pas

1. Vérifiez que PyQt6 est installé :
   ```powershell
   pip install PyQt6
   ```

2. Vérifiez les erreurs dans la console

3. Essayez de lancer en mode debug :
   ```powershell
   python -m src.gui
   ```

### Erreur d'import

Si vous avez des erreurs d'import, assurez-vous d'être dans le répertoire du projet :
```powershell
cd "C:\Users\jrnaz\OneDrive\Desktop\PROJET COMPILER"
```

### PLY non trouvé

Si vous avez des erreurs liées à PLY :
```powershell
pip install ply
```

## 📚 Documentation

- **README.md** - Documentation complète du projet
- **GUI_README.md** - Guide de l'interface graphique
- **FLEX_BISON_INTEGRATION.md** - Guide d'intégration Flex/Bison

## 🎉 C'est parti !

L'application GUI devrait maintenant être ouverte. Si ce n'est pas le cas, utilisez une des méthodes ci-dessus.

**Bon développement ! 🚀**

