%{
/* Fichier Bison (.y) pour l'analyseur syntaxique
 * 
 * Ce fichier définit la grammaire du langage logique.
 * 
 * Compilation:
 *   bison -d parser.y    (génère parser.tab.c et parser.tab.h)
 *   gcc -c parser.tab.c -o parser.tab.o
 */

#include <stdio.h>
#include <stdlib.h>
#include "ast.h"  // Définitions des structures AST

// Déclaration de yylex (générée par Flex)
extern int yylex(void);
extern int yylineno;
extern char* yytext;

// Fonction pour afficher les erreurs
void yyerror(const char* s);
%}

%union {
    int bool_val;        // Pour les booléens (TRUE/FALSE)
    char* string_val;    // Pour les identifiants
    struct Expr* expr;   // Pour les expressions AST
}

%token <bool_val> BOOL
%token <string_val> IDENT
%token AND OR NOT
%token LPAREN RPAREN

%type <expr> expression or_expr and_expr not_expr primary

%left OR          /* Priorité la plus faible */
%left AND
%right NOT         /* Associativité à droite */

%%

/* Grammaire BNF */
expression
    : or_expr
    {
        $$ = $1;
    }
    ;

or_expr
    : and_expr
    {
        $$ = $1;
    }
    | or_expr OR and_expr
    {
        $$ = create_or_expr($1, $3);
    }
    ;

and_expr
    : not_expr
    {
        $$ = $1;
    }
    | and_expr AND not_expr
    {
        $$ = create_and_expr($1, $3);
    }
    ;

not_expr
    : NOT not_expr
    {
        $$ = create_not_expr($2);
    }
    | primary
    {
        $$ = $1;
    }
    ;

primary
    : IDENT
    {
        $$ = create_var_expr($1);
    }
    | BOOL
    {
        $$ = create_bool_expr($1);
    }
    | LPAREN expression RPAREN
    {
        $$ = $2;
    }
    ;

%%

void yyerror(const char* s) {
    fprintf(stderr, "Erreur de parsing à la ligne %d: %s\n", yylineno, s);
    fprintf(stderr, "Token actuel: '%s'\n", yytext);
}

/* Fonction principale pour tester le parser */
int main(int argc, char** argv) {
    if (argc > 1) {
        FILE* file = fopen(argv[1], "r");
        if (!file) {
            fprintf(stderr, "Impossible d'ouvrir le fichier: %s\n", argv[1]);
            return 1;
        }
        yyin = file;
    }
    
    struct Expr* result = NULL;
    int parse_result = yyparse();
    
    if (parse_result == 0) {
        printf("Parsing réussi!\n");
        // Afficher l'AST ou faire autre chose avec result
    } else {
        printf("Erreur de parsing.\n");
        return 1;
    }
    
    return 0;
}

