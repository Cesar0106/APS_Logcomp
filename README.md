# APS_Logcomp - LangueFrancaise

## Intro
A linguagem vai utilizar nomes comuns como if, else e for. No entanto, tudo será traduzido para o francês.

## Dicionário FRANCES INGLES

```
PROGRAMME -> PROGRAM
BLOC -> BLOCK
INSTRUCTION -> INSTRUCTION 
ATTRIBUTION -> ASSIGNMENT
CONDITIONNEL -> CONDITIONAL
VARIABLE -> VARIABLE 
IDENTIFIANT -> IDENTIFIER
EXPRESSION -> EXPRESSION 
COMPARAISON -> COMPARISON
OPERATEUR_LOGIQUE -> LOGICAL_OPERATOR
LETTRE -> LETTER
affiche -> display
var -> var 
entier -> int
chaine -> string
pour -> for
ou -> or
et -> and
si -> if
sinon -> else

```

## EBNF

```
PROGRAMME = { INSTRUCTION } ;

BLOC = "{", { INSTRUCTION }, "}" ;

INSTRUCTION = ( λ | ATTRIBUTION | CONDITIONNEL | BOUCLE | VARIABLE ), "\n" ;

VARIABLE = "var", IDENTIFIANT, "entier", [ "=", EXPRESSION ] ;

ATTRIBUTION = IDENTIFIANT, "=", EXPRESSION ;

CONDITIONNEL = "si", COMPARAISON, BLOC;

BOUCLE = "pour", "(", ATTRIBUTION, ";", COMPARAISON, ";", ATTRIBUTION, ")", BLOC ;

EXPRESSION = TERME, { ( "+" | "-" ), TERME } ;

TERME = FACTEUR, { ( "*" | "/" ), FACTEUR } ;

FACTEUR = NUMBER 
        | IDENTIFIANT 
        | "(", EXPRESSION, ")" ;

COMPARAISON = EXPRESSION, ( "==" | "<" | ">", "&&", "||"), EXPRESSION ;

IDENTIFIANT = LETTRE, { LETTRE | CHIFFRE | "_" } ;

NUMBER = CHIFFRE, { CHIFFRE } ;

LETTRE = "a" | ... | "z" | "A" | ... | "Z" ;

CHIFFRE = "0" | "1" | ... | "9" ;

```
