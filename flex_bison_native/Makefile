# Makefile pour compiler Flex/Bison
#
# Usage:
#   make          # Compile tout
#   make clean    # Nettoie les fichiers générés
#   make test     # Teste le parser

CC = gcc
CFLAGS = -Wall -Wextra -g
FLEX = flex
BISON = bison

# Fichiers sources
LEXER_SRC = lexer.l
PARSER_SRC = parser.y
LEXER_C = lex.yy.c
PARSER_C = parser.tab.c
PARSER_H = parser.tab.h

# Fichiers objets
LEXER_OBJ = lex.yy.o
PARSER_OBJ = parser.tab.o

# Exécutable
TARGET = parser

.PHONY: all clean test

all: $(TARGET)

# Générer le code C depuis Flex
$(LEXER_C): $(LEXER_SRC)
	$(FLEX) $(LEXER_SRC)

# Générer le code C depuis Bison
$(PARSER_C) $(PARSER_H): $(PARSER_SRC)
	$(BISON) -d $(PARSER_SRC)

# Compiler le lexer
$(LEXER_OBJ): $(LEXER_C)
	$(CC) $(CFLAGS) -c $(LEXER_C) -o $(LEXER_OBJ)

# Compiler le parser
$(PARSER_OBJ): $(PARSER_C) $(PARSER_H)
	$(CC) $(CFLAGS) -c $(PARSER_C) -o $(PARSER_OBJ)

# Lier tout ensemble
$(TARGET): $(LEXER_OBJ) $(PARSER_OBJ)
	$(CC) $(CFLAGS) -o $(TARGET) $(LEXER_OBJ) $(PARSER_OBJ) -lfl

# Test
test: $(TARGET)
	@echo "Test du parser..."
	@echo "A AND B" | ./$(TARGET) || true

# Nettoyer
clean:
	rm -f $(LEXER_C) $(PARSER_C) $(PARSER_H)
	rm -f $(LEXER_OBJ) $(PARSER_OBJ)
	rm -f $(TARGET)
	rm -f *.o

# Aide
help:
	@echo "Makefile pour compiler Flex/Bison"
	@echo ""
	@echo "Cibles disponibles:"
	@echo "  make          - Compile le parser"
	@echo "  make clean    - Nettoie les fichiers générés"
	@echo "  make test     - Teste le parser"
	@echo "  make help     - Affiche cette aide"

