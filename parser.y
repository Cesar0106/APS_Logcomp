%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex();
void yyerror(const char *s) { printf("ERROR: %s\n", s); }
%}

%token NUMBER STRING IDENTIFIER SPACE BREAKLINE LEFT_PARENTHESIS RIGHT_PARENTHESIS EQUAL ASSIGN GREATER LESS OR AND NOT PLUS MINUS TIMES DIVIDE SEMICOLON PRINT IF ELSE FOR VAR TYPE HASHTAG LEFT_BRACES RIGHT_BRACES IDENTATION

%start program

%%

program :
    statements
    ;

statements :
    /* vazio */
    | statement BREAKLINE
    | statements statement BREAKLINE
    ;

block :
    LEFT_BRACES statements RIGHT_BRACES BREAKLINE
    ;

statement :
    /* vazio */
    |var_declaration
    | assignment
    | for_loop
    | IF bool_expression block
    ;

var_declaration :
    VAR IDENTIFIER TYPE
    | VAR IDENTIFIER TYPE ASSIGN expression
    ;

assignment :
    IDENTIFIER ASSIGN expression
    | VAR IDENTIFIER TYPE ASSIGN expression
    ;

for_loop :
    FOR LEFT_PARENTHESIS assignment SEMICOLON bool_expression SEMICOLON assignment RIGHT_PARENTHESIS block
    ;

bool_expression :
    expression EQUAL expression
    | expression GREATER expression
    | expression LESS expression
    | bool_expression OR bool_expression
    | bool_expression AND bool_expression
    ;

expression :
    term
    | expression PLUS term
    | expression MINUS term
    ;

term :
    factor
    | term TIMES factor
    | term DIVIDE factor
    ;

factor :
    NUMBER
    | IDENTIFIER
    | STRING
    | LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
    ;

%%

int main() {
    yyparse();
    return 0;
}
