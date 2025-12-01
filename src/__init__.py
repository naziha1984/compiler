"""Package principal du compilateur de langage logique.

Ce package exporte toutes les fonctionnalités principales :
- parse() : Parser une expression
- evaluate() : Évaluer une expression
- optimize() : Optimiser une expression
- AST : Tous les nœuds AST
- Erreurs : Toutes les classes d'erreurs
"""

from . import ast
from .ast import And, BoolLit, Expr, Not, Or, Var, from_json, pretty_print
from .errors import (
    CompilerError,
    EndOfInputError,
    EvaluationError,
    LexicalError,
    MissingOperandError,
    MissingParenthesisError,
    ParseError,
    SourceLocation,
    UnexpectedTokenError,
    UnknownVariableError,
)
from .evaluator import evaluate
from .optimizer import optimize
from .parser import parse
from .pretty import CaseStyle, pretty_print as smart_pretty_print
from .tokenizer import Token, TokenType, debug_tokens, tokenize
from .visitors import DefaultVisitor, ExprVisitor

__all__ = [
    # AST
    "ast",
    "Expr",
    "Var",
    "BoolLit",
    "Not",
    "And",
    "Or",
    "from_json",
    "pretty_print",
    # Parser
    "parse",
    # Evaluator
    "evaluate",
    # Optimizer
    "optimize",
    # Tokenizer
    "tokenize",
    "Token",
    "TokenType",
    "debug_tokens",
    # Errors
    "CompilerError",
    "LexicalError",
    "ParseError",
    "UnexpectedTokenError",
    "MissingParenthesisError",
    "MissingOperandError",
    "EndOfInputError",
    "EvaluationError",
    "UnknownVariableError",
    "SourceLocation",
    # Visitors
    "ExprVisitor",
    "DefaultVisitor",
    # Pretty printer
    "smart_pretty_print",
    "CaseStyle",
]
