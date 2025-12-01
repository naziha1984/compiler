# Icônes Material Icons

Ce dossier contient les icônes Material Design pour l'application.

## Icônes requises

Pour une expérience complète, ajoutez les icônes suivantes (format SVG) :

- `evaluate.svg` - Icône pour le bouton "Évaluer"
- `optimize.svg` - Icône pour le bouton "Optimiser"
- `json.svg` - Icône pour l'onglet JSON
- `ast.svg` - Icône pour l'onglet AST
- `tokens.svg` - Icône pour l'onglet Tokens
- `about.svg` - Icône pour le menu "À propos"
- `theme.svg` - Icône pour le toggle dark/light mode

## Source des icônes

Téléchargez les icônes depuis :
- **Material Icons** : https://fonts.google.com/icons
- **Material Design Icons** : https://materialdesignicons.com/

## Format recommandé

- Format : SVG
- Taille : 24x24px ou 48x48px
- Couleur : Blanc (#FFFFFF) pour le dark mode

## Utilisation dans le code

Les icônes peuvent être chargées dans `gui.py` avec :

```python
from PyQt6.QtGui import QIcon

icon = QIcon("assets/icons/evaluate.svg")
button.setIcon(icon)
```

## Note

Les icônes sont optionnelles. L'application fonctionne parfaitement sans elles, mais elles améliorent l'expérience utilisateur.

