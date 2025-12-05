# Guide d'Intégration Flex/Bison

Ce guide explique comment intégrer Flex/Bison dans ce projet de compilateur Python. Il existe deux approches principales :

## 📋 Table des matières

1. [Approche 1 : PLY (Python Lex-Yacc) - Recommandé](#approche-1--ply-python-lex-yacc---recommandé)
2. [Approche 2 : Flex/Bison natifs (C)](#approche-2--flexbison-natifs-c)
3. [Comparaison des approches](#comparaison-des-approches)
4. [Migration depuis le code actuel](#migration-depuis-le-code-actuel)

---

## Approche 1 : PLY (Python Lex-Yacc) - Recommandé

**PLY** est l'équivalent Python de Flex/Bison. C'est la solution la plus simple et la plus naturelle pour un projet Python.

### Avantages
- ✅ 100% Python, pas de compilation C nécessaire
- ✅ Intégration facile avec le code existant
- ✅ Même syntaxe que Flex/Bison
- ✅ Compatible avec tous les systèmes d'exploitation
- ✅ Facile à déboguer

### Installation

```bash
pip install ply
```

### Structure des fichiers

```
src/
  ├── lexer_ply.py      # Fichier Flex (.l) → PLY
  ├── parser_ply.py     # Fichier Bison (.y) → PLY
  └── ...
```

### Exemple d'implémentation

Voir les fichiers `src/lexer_ply.py` et `src/parser_ply.py` pour une implémentation complète.

### Utilisation

```python
from src.lexer_ply import lexer
from src.parser_ply import parser

# Tokeniser
lexer.input("A AND B")
tokens = []
for token in lexer:
    tokens.append(token)

# Parser
result = parser.parse("A AND B", lexer=lexer)
```

---

## Approche 2 : Flex/Bison natifs (C)

Cette approche utilise les outils Flex/Bison originaux en C, puis les interfacés avec Python via des bindings.

### Avantages
- ✅ Performance maximale (code C compilé)
- ✅ Outils standard de l'industrie
- ✅ Support de grammaires très complexes

### Inconvénients
- ⚠️ Nécessite Flex et Bison installés
- ⚠️ Nécessite un compilateur C
- ⚠️ Plus complexe à configurer
- ⚠️ Portabilité réduite (surtout sur Windows)

### Prérequis

#### Sur Linux/macOS
```bash
# Ubuntu/Debian
sudo apt-get install flex bison

# macOS
brew install flex bison

# Vérifier l'installation
flex --version
bison --version
```

#### Sur Windows
1. Installer **MSYS2** ou **Cygwin**
2. Installer Flex et Bison via le gestionnaire de paquets
3. Ou utiliser **WinFlexBison** : https://github.com/lexxmark/winflexbison

### Structure des fichiers

```
src/
  ├── lexer.l           # Fichier Flex
  ├── parser.y          # Fichier Bison
  ├── parser_wrapper.c  # Wrapper C pour Python
  ├── parser_wrapper.h  # Headers
  └── setup.py          # Script de build avec Cython/ctypes
```

### Processus de build

1. **Générer le code C depuis Flex/Bison** :
   ```bash
   flex lexer.l          # Génère lex.yy.c
   bison -d parser.y     # Génère parser.tab.c et parser.tab.h
   ```

2. **Compiler en bibliothèque partagée** :
   ```bash
   gcc -shared -fPIC -o parser.so lex.yy.c parser.tab.c parser_wrapper.c -lfl
   ```

3. **Interfacer avec Python** (via ctypes ou Cython)

### Exemple de fichiers

Voir les fichiers dans `flex_bison_native/` pour des exemples complets.

---

## Comparaison des approches

| Critère | PLY | Flex/Bison natifs |
|---------|-----|-------------------|
| **Facilité d'installation** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Performance** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Portabilité** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Maintenance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Compatibilité Python** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Recommandation** | ✅ **Pour ce projet** | Pour projets très performants |

**Recommandation :** Utilisez **PLY** pour ce projet. C'est plus simple, plus portable, et les performances sont largement suffisantes.

---

## Migration depuis le code actuel

### Étape 1 : Installer PLY

```bash
pip install ply
```

### Étape 2 : Créer les fichiers PLY

Créez `src/lexer_ply.py` et `src/parser_ply.py` (voir exemples fournis).

### Étape 3 : Adapter l'interface

Les nouveaux parsers PLY doivent avoir la même interface que l'ancien :

```python
# Ancien code
from src.parser import parse
expr = parse("A AND B")

# Nouveau code (même interface)
from src.parser_ply import parse
expr = parse("A AND B")
```

### Étape 4 : Mettre à jour les imports

Modifiez `src/__init__.py` pour utiliser les nouveaux parsers :

```python
# Option 1 : Remplacer complètement
from .parser_ply import parse

# Option 2 : Garder les deux (avec flag)
from .parser import parse as parse_old
from .parser_ply import parse as parse_ply

def parse(source: str, use_ply: bool = True):
    if use_ply:
        return parse_ply(source)
    return parse_old(source)
```

### Étape 5 : Tester

```bash
pytest tests/
```

---

## Fichiers de référence

- `src/lexer_ply.py` - Implémentation PLY du lexer
- `src/parser_ply.py` - Implémentation PLY du parser
- `flex_bison_native/lexer.l` - Fichier Flex natif (exemple)
- `flex_bison_native/parser.y` - Fichier Bison natif (exemple)
- `flex_bison_native/Makefile` - Makefile pour compiler Flex/Bison

---

## Ressources

- **PLY Documentation** : https://www.dabeaz.com/ply/
- **Flex Manual** : https://www.gnu.org/software/flex/manual/
- **Bison Manual** : https://www.gnu.org/software/bison/manual/
- **Python C Extensions** : https://docs.python.org/3/extending/extending.html

---

## Support

Pour toute question sur l'intégration Flex/Bison, consultez :
1. Ce guide
2. Les fichiers d'exemple fournis
3. La documentation officielle de PLY/Flex/Bison

