# Guide d'utilisation de l'interface graphique

## 🖥️ Application Desktop PyQt6

L'application graphique fournit une interface complète et moderne pour utiliser le compilateur de langage logique.

## 🚀 Lancement

```bash
python -m src.gui
```

## 🎨 Thème Dark Mode

L'application utilise un **thème sombre professionnel** basé sur Material Design :
- Fond principal : `#121212`
- Cartes/secondaires : `#1E1E1E`
- Texte : `#EEEEEE`
- Accent bleu : `#2196F3`
- Boutons verts : `#43A047`

Le thème est appliqué automatiquement au lancement.

## 📋 Fonctionnalités

### 1. Saisie d'expression avec colorisation syntaxique

Dans le champ **"Expression logique"**, vous pouvez saisir :
- Expressions simples : `A AND B`
- Avec parenthèses : `(A OR B) AND C`
- Avec NOT : `NOT (A AND B)`
- Avec booléens : `TRUE AND FALSE`
- Avec commentaires : `A AND B  # commentaire`

**Colorisation automatique :**
- Mots-clés (AND, OR, NOT, TRUE, FALSE) : **Bleu clair**
- Variables : **Blanc**
- Parenthèses : **Jaune**
- Commentaires : **Gris italique**
- Erreurs : **Rouge souligné**

### 2. Environnement de variables

Dans le champ **"Environnement"**, définissez les valeurs des variables :
- Format : `A=true,B=false,C=true`
- Valeurs acceptées : `true`, `false`, `1`, `0`, `yes`, `no`, `on`, `off`

### 3. Boutons d'action

- **Évaluer** : Parse, affiche tous les résultats et évalue l'expression
- **Optimiser** : Parse, optimise l'expression et affiche le résultat optimisé

### 4. Onglets de visualisation

L'application affiche les résultats dans 6 onglets avec **animations fade-in** :

#### 📝 Tokens
Affiche la liste des tokens générés par le tokenizer avec leurs positions.

#### 🌳 AST
Affiche l'arbre syntaxique abstrait (AST) brut formaté.

#### ✨ Pretty-Printer
Affiche l'expression formatée de manière lisible avec minimisation des parenthèses.

#### ⚡ AST Optimisé
Affiche l'AST après optimisation (constant folding).

#### 📄 JSON
Affiche la représentation JSON de l'AST pour export/sérialisation.

#### 🎨 Graphviz
Affiche une visualisation graphique de l'AST (nécessite Graphviz installé).

**Bouton "Exporter Graphviz (PNG)"** : Exporte le graphique en fichier PNG.

### 5. Mode auto-évaluation en temps réel

Activez le mode **"Évaluation en temps réel"** dans le menu **Options** :
- Dès que vous tapez, l'expression est automatiquement parsée et évaluée
- Délai de 500ms après la dernière frappe pour éviter les calculs inutiles
- Mise à jour automatique de tous les onglets

### 6. Drag & Drop de fichiers

**Glissez-déposez** un fichier `.txt`, `.expr` ou `.logical` dans la fenêtre :
- Le contenu du fichier est automatiquement chargé dans le champ d'expression
- Si l'auto-évaluation est activée, l'expression est évaluée automatiquement

**Ou utilisez le menu Fichier → Charger un fichier...**

### 7. Menu

#### Fichier
- **Charger un fichier...** : Charge une expression depuis un fichier
- **Quitter** : Ferme l'application

#### Options
- **Évaluation en temps réel** : Active/désactive l'auto-évaluation

#### Aide
- **À propos** : Affiche la fenêtre "À propos" avec les informations du projet

## ⚠️ Gestion des erreurs

En cas d'erreur :
1. Un message d'erreur apparaît en bas de la fenêtre (zone rouge)
2. La position de l'erreur est **surlignée en rouge** dans le champ d'expression
3. Une boîte de dialogue détaillée s'affiche avec :
   - Le type d'erreur
   - La position (ligne/colonne)
   - Le contexte de l'erreur
   - Des suggestions si disponibles

## 💡 Exemples d'utilisation

### Exemple 1 : Expression simple
```
Expression: A AND B
Environnement: A=true,B=false
Résultat: False
```

### Exemple 2 : Expression complexe
```
Expression: (A OR B) AND NOT C
Environnement: A=false,B=true,C=true
Résultat: False
```

### Exemple 3 : Optimisation
```
Expression: TRUE AND A
Environnement: A=true
Résultat optimisé: A (TRUE AND X → X)
```

### Exemple 4 : Drag & Drop
1. Créez un fichier `test.expr` avec le contenu : `A AND (B OR C)`
2. Glissez le fichier dans la fenêtre
3. L'expression est automatiquement chargée

## ⌨️ Raccourcis clavier

- **Ctrl+O** : Charger un fichier (si implémenté)
- **Tab** : Navigation entre les champs
- **Entrée** : Évalue l'expression (si focus sur le bouton)

## 🎞️ Animations

L'application utilise des animations fluides :
- **Fade-in** lors du changement d'onglet (200ms)
- **Slide-from-bottom** lors de la mise à jour des résultats (300ms)

## 🎨 Graphviz

Pour visualiser les AST avec Graphviz :

1. **Installer Graphviz** :
   - Windows : Télécharger depuis https://graphviz.org/download/
   - Linux : `sudo apt-get install graphviz`
   - macOS : `brew install graphviz`

2. **Utiliser l'onglet Graphviz** :
   - L'AST est automatiquement généré et affiché
   - Cliquez sur "Exporter Graphviz (PNG)" pour sauvegarder

## 🔧 Dépannage

### L'application ne se lance pas
- Vérifiez que PyQt6 est installé : `pip install PyQt6`
- Vérifiez que vous êtes dans le bon répertoire

### Les erreurs ne s'affichent pas correctement
- Vérifiez que le fichier `src/style.qss` existe
- Les erreurs s'affichent aussi dans la console

### Graphviz ne fonctionne pas
- Vérifiez que Graphviz est installé et dans le PATH
- Le message d'erreur dans l'onglet Graphviz vous indiquera si Graphviz est manquant

### L'auto-évaluation est trop lente
- Le délai de 500ms peut être ajusté dans le code (ligne `self.auto_eval_timer.start(500)`)
- Désactivez l'auto-évaluation si vous préférez évaluer manuellement

## 📚 Pour aller plus loin

Consultez le `README.md` principal pour :
- La grammaire du langage
- Les détails techniques
- L'utilisation en ligne de commande
- L'API Python
