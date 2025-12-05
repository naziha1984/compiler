# Flex/Bison Natifs - Exemples

Ce dossier contient des exemples de fichiers Flex/Bison natifs (en C) pour le langage logique.

## 📁 Fichiers

- `lexer.l` - Fichier Flex pour l'analyseur lexical
- `parser.y` - Fichier Bison pour l'analyseur syntaxique
- `Makefile` - Makefile pour compiler les fichiers
- `README.md` - Ce fichier

## 🔧 Prérequis

### Linux/macOS

```bash
# Ubuntu/Debian
sudo apt-get install flex bison gcc

# macOS
brew install flex bison gcc
```

### Windows

1. Installer **MSYS2** : https://www.msys2.org/
2. Dans MSYS2 :
   ```bash
   pacman -S flex bison gcc
   ```

Ou utiliser **WinFlexBison** : https://github.com/lexxmark/winflexbison

## 🚀 Compilation

```bash
# Compiler
make

# Nettoyer
make clean

# Tester
make test
```

## 📝 Notes

Ces fichiers sont des **exemples de référence**. Pour une intégration complète avec Python, vous devrez :

1. Créer un wrapper C pour interfacer avec Python (via ctypes ou Cython)
2. Compiler en bibliothèque partagée (`.so` sur Linux, `.dll` sur Windows, `.dylib` sur macOS)
3. Créer des bindings Python pour appeler les fonctions C

**Recommandation :** Pour ce projet Python, utilisez plutôt **PLY** (voir `src/lexer_ply.py` et `src/parser_ply.py`), qui est plus simple et plus portable.

## 🔗 Ressources

- [Flex Manual](https://www.gnu.org/software/flex/manual/)
- [Bison Manual](https://www.gnu.org/software/bison/manual/)
- [Python C Extensions](https://docs.python.org/3/extending/extending.html)

