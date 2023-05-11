<pre>
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


IDENT: [a-zA-Z_][a-zA-Z_0-9]*;
INT: [0-9]+;
SET: '{' '}' // пустое множество
    |  '{' ELEM (',' ELEM)* '}';
ELEM: INT | INT '..' INT;
STRING: '"' (IDENT | ' ' )* '"';
</pre>



### Примеры

<pre>
let g1 = load 'wine.dot';
let g = set_start {0..100}) of set_final (get_vertices g1) of g1;

let l1 = "l1" | "l2";
let q1 = ("type" | l1)*;


let q2 = "sub_class_of" + l1;

let res1 = g & q1;
let res2 = g & q2;


print res1;

let s = get_start g;

let vertices1 = filter (map (edges of res1) with ((u_g, u_q1), l, (v_g, v_q1)) => u_g) with v => v in s;
let vertices1 = filter (map (edges of res2) with ((u_g, u_q2), l, (v_g, v_q2)) => u_g) with (v => v in s);

let vertices = vertices1 & vertices2;
print vertices;
</pre>
