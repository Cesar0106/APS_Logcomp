# APS_Logcomp - LangueFrancaise

## Intro
A linguagem vai utilizar nomes comuns como if, else e for. No entanto, tudo será traduzido para o francês.

## Dicionário FRANCES INGLES

PROGRAMME -> PROGRAM
BLOC -> BLOCK
INSTRUCTION -> INSTRUCTION 
ATTRIBUTION -> ASSIGNMENT
IMPRIME -> PRINT
CONDITIONNEL -> CONDITIONAL
BOUCLE -> LOOP
VARIABLE -> VARIABLE 
IDENTIFIANT -> IDENTIFIER
EXPRESSION -> EXPRESSION 
TERME -> TERM
FACTEUR -> FACTOR
COMPARAISON -> COMPARISON
OPERATEUR_LOGIQUE -> LOGICAL_OPERATOR
NOMBRE -> NUMBER
LETTRE -> LETTER
CHIFFRE -> DIGIT
affiche -> display
var -> var 
entier -> int
chaine -> string
pour -> for
ou -> or
et -> and
si -> if
sinon -> else

## EBNF

PROGRAMME = { INSTRUCTION };

BLOC = { "{", INSTRUCTION, "}"};

INSTRUCTION = ( λ | ATTRIBUTION | IMPRIME | CONDITIONNEL | BOUCLE | VARIABLE ), "\n" ;

ATTRIBUTION = IDENTIFIANT, "=", EXPRESSION;

IMPRIME = "affiche", "#", EXPRESSION, "#";

EXPRESSION = TERME, {("+" | "-" | "."), TERME};

TERME = FACTEUR, {("*" | "/"), FACTEUR };

FACTEUR = (("+" | "-" | "!"), FACTEUR | NOMBRE | LETTRE | "(", EXPRESSION, ")" | IDENTIFIANT | ENTREE, "(", ")");

COMPARAISON = (EXPRESSION, ("==" | "<" | ">" | "<=" | ">="), EXPRESSION);

OPERATEUR_LOGIQUE = (EXPRESSION, ("ou" | "et"), EXPRESSION);

VARIABLE = "var", IDENTIFIANT, { "entier" | "chaine" | "=", EXPRESSION};

BOUCLE = "pour", ATTRIBUTION, ";", EXPRESSION, ";", ATTRIBUTION, BLOC;

CONDITIONNEL = "si", EXPRESSION, BLOC, ["sinon", BLOC];

IDENTIFIANT = LETTRE, { LETTRE | CHIFFRE | "_"};

NOMBRE = CHIFFRE, { CHIFFRE };

LETTRE = ( a | ... | z | A | .. | Z);

CHIFFRE = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
