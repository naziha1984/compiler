"""Script de test pour vérifier l'intégration PLY.

Ce script teste les nouveaux parsers PLY et compare avec l'ancien parser.
"""

from __future__ import annotations

from src import parse as parse_old
from src.parser_ply import parse as parse_ply
from src.lexer_ply import tokenize_ply


def test_lexer_ply() -> None:
    """Test du lexer PLY."""
    print("=" * 60)
    print("Test du Lexer PLY")
    print("=" * 60)

    test_cases = [
        "A AND B",
        "A OR B OR C",
        "NOT A",
        "(A OR B) AND C",
        "TRUE AND FALSE",
        "A AND B # commentaire",
    ]

    for test in test_cases:
        print(f"\nInput: {test}")
        try:
            tokens = tokenize_ply(test)
            print(f"  Tokens ({len(tokens)}):")
            for token in tokens:
                print(f"    {token.type:10} = {token.value!r} (ligne {token.lineno})")
        except Exception as e:
            print(f"  ERREUR: {e}")


def test_parser_ply() -> None:
    """Test du parser PLY."""
    print("\n" + "=" * 60)
    print("Test du Parser PLY")
    print("=" * 60)

    test_cases = [
        ("A AND B", True),
        ("A OR B", True),
        ("NOT A", True),
        ("(A OR B) AND C", True),
        ("NOT (A AND B)", True),
        ("TRUE AND FALSE", True),
        ("A OR TRUE", True),
        ("A AND", False),  # Erreur attendue
        ("A & B", False),  # Erreur attendue
    ]

    for test, should_succeed in test_cases:
        print(f"\nTest: {test}")
        try:
            result_ply = parse_ply(test)
            if should_succeed:
                print(f"  ✓ PLY: {result_ply}")
            else:
                print(f"  ✗ PLY: Devrait échouer mais a réussi: {result_ply}")
        except Exception as e:
            if should_succeed:
                print(f"  ✗ PLY: Erreur inattendue: {e}")
            else:
                print(f"  ✓ PLY: Erreur attendue: {type(e).__name__}")


def test_comparison() -> None:
    """Compare les résultats du parser PLY avec l'ancien parser."""
    print("\n" + "=" * 60)
    print("Comparaison Parser PLY vs Ancien Parser")
    print("=" * 60)

    test_cases = [
        "A AND B",
        "A OR B",
        "NOT A",
        "(A OR B) AND C",
        "NOT (A AND B)",
        "TRUE AND FALSE",
        "A OR TRUE",
    ]

    for test in test_cases:
        print(f"\nTest: {test}")
        try:
            result_old = parse_old(test)
            result_ply = parse_ply(test)
            if result_old == result_ply:
                print(f"  ✓ Résultats identiques: {result_old}")
            else:
                print(f"  ✗ Résultats différents:")
                print(f"    Ancien: {result_old}")
                print(f"    PLY:    {result_ply}")
        except Exception as e_old:
            try:
                result_ply = parse_ply(test)
                print(f"  ✗ Ancien échoue mais PLY réussit:")
                print(f"    Ancien: {e_old}")
                print(f"    PLY:    {result_ply}")
            except Exception as e_ply:
                print(f"  ✓ Les deux échouent (attendu):")
                print(f"    Ancien: {type(e_old).__name__}")
                print(f"    PLY:    {type(e_ply).__name__}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Tests d'intégration PLY")
    print("=" * 60)

    try:
        test_lexer_ply()
        test_parser_ply()
        test_comparison()
        print("\n" + "=" * 60)
        print("Tests terminés!")
        print("=" * 60)
    except ImportError as e:
        print(f"\nERREUR: Impossible d'importer PLY. Installez-le avec:")
        print("  pip install ply")
        print(f"\nDétails: {e}")

