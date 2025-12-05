%{
/* Fichier Flex (.l) pour l'analyseur lexical
 * 
 * Ce fichier définit les règles de tokenisation pour le langage logique.
 * 
 * Compilation:
 *   flex lexer.l
 *   gcc -c lex.yy.c -o lex.yy.o
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.tab.h"  // Généré par Bison, contient les définitions de tokens

// Variables globales pour le tracking de position
extern int yylineno;
extern char* yytext;
extern FILE* yyin;

// Fonction pour convertir un token en string (pour debug)
const char* token_name(int token);
%}

%option yylineno
%option case-insensitive
%option noyywrap

%%

[ \t]+          { /* Ignorer les espaces et tabulations */ }

#.*             { /* Ignorer les commentaires (# jusqu'à la fin de la ligne) */ }

\n              { /* Nouvelle ligne (yylineno est géré automatiquement) */ }

"("             { return LPAREN; }
")"             { return RPAREN; }

"AND"           { return AND; }
"OR"            { return OR; }
"NOT"           { return NOT; }

"TRUE"          { yylval.bool_val = 1; return BOOL; }
"FALSE"         { yylval.bool_val = 0; return BOOL; }

[A-Za-z_][A-Za-z0-9_]* {
    // Identifiant ou mot-clé
    // Les mots-clés ont déjà été matchés par les règles précédentes
    yylval.string_val = strdup(yytext);
    return IDENT;
}

.               { 
    fprintf(stderr, "Erreur lexicale à la ligne %d: caractère inattendu '%c'\n", 
            yylineno, yytext[0]);
    return -1;
}

%%

// Fonction utilitaire pour obtenir le nom d'un token
const char* token_name(int token) {
    switch(token) {
        case IDENT: return "IDENT";
        case BOOL: return "BOOL";
        case AND: return "AND";
        case OR: return "OR";
        case NOT: return "NOT";
        case LPAREN: return "LPAREN";
        case RPAREN: return "RPAREN";
        case 0: return "EOF";
        default: return "UNKNOWN";
    }
}

