%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.tab.h"
%}

DIGIT [0-9]
LETTER [a-zA-Z]

%%

"\t"|"    "  { /* Ignore identation */ }
"\n" { printf("BREAKLINE\n"); return BREAKLINE; }
"(" { printf("LEFT_PARENTHESIS\n"); return LEFT_PARENTHESIS; }
")" { printf("RIGHT_PARENTHESIS\n"); return RIGHT_PARENTHESIS; }
"==" { printf("EQUAL\n"); return EQUAL; }
"=" { printf("ASSIGN\n"); return ASSIGN; }
">" { printf("GREATER\n"); return GREATER; }
"<" { printf("LESS\n"); return LESS; }
"||" { printf("OR\n"); return OR; }
"&&" { printf("AND\n"); return AND; }
"!" { printf("NOT\n"); return NOT; }
"+" { printf("PLUS\n"); return PLUS; }
"-" { printf("MINUS\n"); return MINUS; }
"*" { printf("TIMES\n"); return TIMES; }
"/" { printf("DIVIDE\n"); return DIVIDE; }
";" { printf("SEMICOLON\n"); return SEMICOLON; }
"si" { printf("IF\n"); return IF; }
"sinon" { printf("ELSE\n"); return ELSE; }
"pour" { printf("FOR\n"); return FOR; }
"entier" { printf("TYPE\n"); return TYPE; }
"var" { printf("VAR\n"); return VAR; }
"#" { printf("HASHTAG\n"); return HASHTAG; }
"{" { printf("LEFT_BRACES\n"); return LEFT_BRACES; }
"}" { printf("RIGHT_BRACES\n"); return RIGHT_BRACES; }
" " {}


{DIGIT}+ { printf("NUMBER\n"); return NUMBER; }
\"(\\.|[^\"\n])*\" { printf("STRING\n"); return STRING; }
[a-zA-Z_][_a-zA-Z0-9]* { printf("IDENTIFIER\n"); return IDENTIFIER; }

.  { printf("Unknown token: %s (ASCII: %d)\n", yytext, (int)yytext[0]); yyterminate(); };

%%