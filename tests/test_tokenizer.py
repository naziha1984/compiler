"""Tests pour le tokenizer amélioré."""

import pytest

from src.errors import LexicalError
from src.tokenizer import TokenType, debug_tokens, tokenize


def test_tokenize_simple_identifier_and_keywords():
    tokens = tokenize("A and B Or not C TRUE false")
    kinds = [t.type for t in tokens]
    lexemes = [t.lexeme for t in tokens]

    assert kinds[:-1] == [
        TokenType.IDENT,
        TokenType.AND,
        TokenType.IDENT,
        TokenType.OR,
        TokenType.NOT,
        TokenType.IDENT,
        TokenType.BOOL,
        TokenType.BOOL,
    ]
    # Identifiants conservent la casse, mots-clés sont upper-case ou normalisés
    assert lexemes[0] == "A"
    assert lexemes[1] == "AND"
    assert lexemes[3] == "OR"
    assert lexemes[4] == "NOT"
    assert lexemes[6] == "TRUE"
    assert lexemes[7] == "FALSE"


def test_tokenize_parentheses_and_positions():
    source = "(A AND (B OR C))"
    tokens = tokenize(source)
    types = [t.type for t in tokens]
    assert types[0] == TokenType.LPAREN  # (
    assert types[1] == TokenType.IDENT   # A
    assert types[2] == TokenType.AND     # AND
    assert types[3] == TokenType.LPAREN  # (
    assert types[4] == TokenType.IDENT   # B
    assert types[5] == TokenType.OR      # OR
    assert types[6] == TokenType.IDENT   # C
    assert types[7] == TokenType.RPAREN  # )
    assert types[8] == TokenType.RPAREN  # )
    assert tokens[-1].type == TokenType.EOF
    # Vérifier les positions (line/column tracking)
    assert tokens[0].location.line == 1
    assert tokens[0].location.column == 1
    assert tokens[0].position == source.index("(")


def test_tokenize_unexpected_character():
    with pytest.raises(LexicalError) as exc_info:
        tokenize("A & B")
    assert "&" in str(exc_info.value)
    # Vérifier que l'erreur a une location
    assert exc_info.value.location is not None
    assert exc_info.value.location.line == 1
    assert exc_info.value.location.column == 3


def test_tokenize_comments():
    # Test avec commentaires
    tokens = tokenize("A AND B # comment here\nC")
    types = [t.type for t in tokens]
    # Le commentaire devrait être ignoré
    assert TokenType.IDENT in types
    assert types[0] == TokenType.IDENT  # A
    # C devrait être présent après le commentaire
    assert any(t.type == TokenType.IDENT and t.lexeme == "C" for t in tokens)


def test_tokenize_line_column_tracking():
    source = "A\nB\nC"
    tokens = tokenize(source)
    # A est à la ligne 1, colonne 1
    assert tokens[0].location.line == 1
    assert tokens[0].location.column == 1
    # B est à la ligne 2, colonne 1
    assert tokens[1].location.line == 2
    assert tokens[1].location.column == 1
    # C est à la ligne 3, colonne 1
    assert tokens[2].location.line == 3
    assert tokens[2].location.column == 1


def test_tokenize_disable_comments():
    # Test avec commentaires désactivés
    from src.tokenizer import Lexer

    # Le # devrait causer une erreur lexicale quand les commentaires sont désactivés
    lexer = Lexer("A # comment", enable_comments=False)
    with pytest.raises(LexicalError):
        lexer.tokenize()


def test_debug_tokens_format():
    tokens = tokenize("A AND TRUE")
    s = debug_tokens(tokens)
    assert "IDENT" in s and "AND" in s and "BOOL" in s


def test_error_formatting():
    """Test que les erreurs peuvent être formatées avec contexte."""
    try:
        tokenize("A & B")
    except LexicalError as e:
        formatted = e.format_error()
        assert "Caractère inattendu" in formatted
        assert "&" in formatted
