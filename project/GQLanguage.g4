grammar GQLanguage;

program: (stmt ';')* EOF;

pattern: var                             # varPattern
        | '(' pattern (',' pattern)* ')' # setPattern;
bind: 'let' name=pattern '=' body=expr;
print: 'print' value=expr;

stmt: bind | print;

intLiteral: INT;
stringLiteral: STRING;
setLiteral: '{' '}'                # emptySet
    |  '{' elem (',' elem)* '}'    # notEmptySet;

elem: el=intLiteral                           #elSet
      | from=intLiteral '..' to=intLiteral    #rangeSet;

val: stringLiteral | intLiteral | setLiteral;
var: IDENT;

lambda: args=pattern '=>' body=expr   #lambdaLiteral
        |  '(' internalLambda=lambda ')'   #lambdaParens;

expr:
    '{' el1=expr (',' el=expr)* '}'                  # exprSet
    | 'set_start' states=expr 'of' automaton=expr               # exprSetStart
    | 'set_final' states=expr 'of' automaton=expr                # exprSetFinal
    | 'add_start' states=expr 'of' automaton=expr                # exprAddStart
    | 'add_finals' states=expr 'of' automaton=expr               # exprAddFinals
    | 'get_start' automaton=expr                          # exprGetStart
    | 'get_final' automaton=expr                          # exprGetFinal
    | 'get_reachable' automaton=expr                      # exprGetReachable
    | 'get_vertices' automaton=expr                       # exprGetVertices
    | 'get_edges' automaton=expr                          # exprGetEdges
    | 'get_labels' automaton=expr                         # exprGetLabels
    | 'map' usedSet=expr 'with' func=lambda                  # exprMap
    | 'filter' usedSet=expr 'with' func=lambda               # exprFilter
    | 'load' name=stringLiteral                             # exprLoad
    | left=expr '&' right=expr                             # exprIntersect
    | left=expr '|' right=expr                             # exprUnion
    | left=expr '+' right=expr                             # exprConcat
    | first=expr '*'                                  # exprKleene
    | left=expr 'in' right=expr                            # exprContains
    | '(' internalExpr=expr ')'                              # exprParens
    | val                                       # exprVal
    | var                                         # exprVar;

COMMENT: ('//' ~[\n]* | '/*' .*? '*/') -> skip;
WS: [ \t\n\r]+ -> channel(HIDDEN);
IDENT: [a-zA-Z_][a-zA-Z_0-9]*;
INT: [0-9]+;
STRING: '"' (~["\\] | '\\' ["\\tvbn])* '"';
