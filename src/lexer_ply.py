"""Analyseur lexical avec PLY (équivalent Python de Flex).

Ce module remplace tokenizer.py en utilisant PLY pour générer le lexer.
PLY utilise la même syntaxe que Flex, mais génère du code Python pur.
"""

from __future__ import annotations

import ply.lex as lex
from typing import Any

from .errors import LexicalError, SourceLocation


# Liste des noms de tokens (requis par PLY)
tokens = (
    "IDENT",
    "BOOL",
    "AND",
    "OR",
    "NOT",
    "LPAREN",
    "RPAREN",
)

# Tokens simples (caractères uniques)
t_LPAREN = r"\("
t_RPAREN = r"\)"

# Ignorer les espaces et tabulations
t_ignore = " \t"

# Ignorer les commentaires (# jusqu'à la fin de la ligne)
def t_COMMENT(t: lex.LexToken) -> None:
    r"#.*"
    # Ne retourne rien, donc le token est ignoré
    pass


# Règle pour les identifiants et mots-clés
def t_IDENT(t: lex.LexToken) -> lex.LexToken:
    r"[A-Za-z_][A-Za-z0-9_]*"
    # Vérifier si c'est un mot-clé
    keywords = {
        "AND": "AND",
        "OR": "OR",
        "NOT": "NOT",
        "TRUE": "BOOL",
        "FALSE": "BOOL",
    }
    upper = t.value.upper()
    if upper in keywords:
        t.type = keywords[upper]
        if t.type == "BOOL":
            # Pour les booléens, on normalise la casse
            t.value = upper
    else:
        # C'est un identifiant, on garde la casse originale
        t.type = "IDENT"
    return t


# Règle pour les nouvelles lignes (pour tracker les lignes)
def t_newline(t: lex.LexToken) -> None:
    r"\n+"
    t.lexer.lineno += len(t.value)


# Gestion des erreurs
def t_error(t: lex.LexToken) -> None:
    """Gère les caractères invalides."""
    # Calculer la colonne (trouver le début de la ligne actuelle)
    line_start = t.lexer.lexdata.rfind("\n", 0, t.lexpos)
    if line_start == -1:
        column = t.lexpos + 1
    else:
        column = t.lexpos - line_start
    location = SourceLocation(
        line=t.lineno,
        column=column,
        offset=t.lexpos,
    )
    raise LexicalError(
        f"Caractère inattendu '{t.value[0]}'",
        location=location,
        source=t.lexer.lexdata,
    )


# Créer le lexer
lexer = lex.lex()


def tokenize_ply(source: str) -> list[lex.LexToken]:
    """Tokenise une chaîne source avec PLY.

    Args:
        source: Code source à tokeniser

    Returns:
        Liste des tokens PLY

    Raises:
        LexicalError: Si un caractère invalide est rencontré
    """
    lexer.input(source)
    tokens: list[lex.LexToken] = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    return tokens


# Fonction de compatibilité avec l'ancien tokenizer
def tokenize(source: str, enable_comments: bool = True) -> list[Any]:
    """Fonction de compatibilité avec l'ancien tokenizer.

    Args:
        source: Code source à tokeniser
        enable_comments: Si True, les commentaires sont ignorés (toujours activé avec PLY)

    Returns:
        Liste des tokens (format PLY)
    """
    return tokenize_ply(source)


if __name__ == "__main__":
    # Test du lexer
    test_input = "A AND (B OR NOT C) # commentaire"
    print(f"Input: {test_input}")
    print("\nTokens:")
    for token in tokenize_ply(test_input):
        print(f"  {token.type:10} = {token.value!r} (ligne {token.lineno}, pos {token.lexpos})")

