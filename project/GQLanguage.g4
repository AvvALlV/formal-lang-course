grammar GQLanguage;

program: (stmt ';')* EOF;

pattern: var | '(' pattern (',' pattern)* ')';
bind: 'let' pattern '=' expr;
print: 'print' expr;

stmt: bind | print;

val: STRING | INT | SET;
var: IDENT;

lambda: pattern '=>' expr | '(' lambda ')';

expr:
    var
    | val
    | 'set_start' expr 'of'  expr
    | 'set_final' expr 'of' expr
    | 'add_start' expr 'of' expr
    | 'add_finals' expr 'of' expr
    | 'get_start' expr
    | 'get_final' expr
    | 'get_reachable' expr
    | 'get_vertices' expr
    | 'get_edges' expr
    | 'get_labels' expr
    | 'map' expr 'with' lambda
    | 'filter' expr 'with' lambda
    | 'load' STRING
    | expr '&' expr // пересечение
    | expr '|' expr // объединение
    | expr '+' expr // конкатенация
    | expr '*'  // замыкание
    | expr '<<' expr // единичиный переход
    | expr 'in' expr // проверка на вхождение
    | '{' expr (',' expr)* '}'
    | '(' expr ')';


COMMENT: ('//' ~[\n]* | '/*' .*? '*/') -> skip;
WS: [ \t\n\r]+ -> channel(HIDDEN);
IDENT: [a-zA-Z_][a-zA-Z_0-9]*;
INT: [0-9]+;
SET: '{' '}' // пустое множество
    |  '{' ELEM (',' ELEM)* '}';
ELEM: INT | INT '..' INT;
STRING: '"' (~["\\] | '\\' ["\\tvbn])* '"';
