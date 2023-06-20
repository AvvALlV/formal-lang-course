import io

import pytest

from project.interpreter.interpreter import *
from textwrap import dedent


def interpret(text: str) -> str:
    parser = parse(text)
    parser.removeErrorListeners()
    tree = parser.program()

    with io.StringIO() as writer:
        visitor = Visitor(writer)
        value = visitor.visit(tree)

        return writer.getvalue()


def test_empty():
    assert interpret("") == ""


def test_exec_simple():
    assert interpret('print "Hello world"') == "Hello world\n"
    assert interpret("print True") == "True\n"
    assert interpret("print 1;") == "1\n"
    assert interpret("print {1, 2};") == "{1, 2}\n"
    assert interpret("print 1 in {1, 2};") == "True\n"
    assert interpret("print 0 in {1, 2};") == "False\n"
    assert interpret("let x = 1; print x in {1, 2};") == "True\n"
    assert interpret("let x = 0; print x in {1, 2};") == "False\n"


def test_discard_simple():
    assert interpret('print 1 in {"asdf"};') == "False\n"
    assert interpret('let x = 1; print x in {"asdf"};') == "False\n"


@pytest.mark.parametrize(
    "left, operation, right, expected",
    [
        ("{1, 2, 3, 4, 5} ", "&", " {2, 3, 4}", {2, 3, 4}),
        ("{1, 2, 3, 4, 5}", "&", "{7, 8, 9}", {}),
        ("{7, 8, 9}", "&", "{}", {}),
        ("{}", "&", "{}", {}),
        ("{1, 2, 3}", "|", "{4, 5, 6}", {1, 2, 3, 4, 5, 6}),
        ("{1, 2, 3, 4, 5}", "|", "{4, 5, 6, 7}", {1, 2, 3, 4, 5, 6, 7}),
        ("{}", "|", "{}", {}),
    ],
)
def test_intersect_union(left, operation, right, expected):
    expr = "print " + left + operation + right + ";"

    actual = interpret(expr)
    expected = Set(expected)

    assert actual == str(expected._set) + "\n"


@pytest.mark.parametrize(
    "left, right, expected",
    [("2", "{1..10}", "True\n"), ("0", "{}", "False\n"), ("9", "{10..13}", "False\n")],
)
def test_in(left, right, expected):
    expr = "print " + left + " in " + right + ";"

    actual = interpret(expr)

    assert actual == expected


@pytest.mark.parametrize(
    "initial, func, expected",
    [
        ("{1, 2}", "x => x in {2}", "{False, True}\n"),
        ("{1, 2, 3}", "x => 5", "{5}\n"),
        ("{1, 2, 3, 4, 5}", "_ => 0", "{0}\n"),
    ],
)
def test_map(initial, func, expected):
    expr = f"print map ({initial}) with {func};"
    actual = interpret(expr)

    assert actual == expected


@pytest.mark.parametrize(
    "initial, func, expected_set",
    [
        ("{1, 2, 3, 4, 5}", "x => x in {2..4}", "{2, 3, 4}\n"),
        ("{1, 2, 3, 4, 5}", "_ => True", "{1, 2, 3, 4, 5}\n"),
        ("{1, 2, 3, 4, 5}", "_ => False", "{}\n"),
    ],
)
def test_filter(initial, func, expected_set):
    expr = f"print filter ({initial}) with {func};"
    actual = interpret(expr)

    assert actual == expected_set


program1 = 'let g = load "skos";' "print get_vertices g;"


def test_automaton1():
    res = interpret(program1)

    assert (
        res
        == "{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143}\n"
    )


program2 = (
    'let g = load "skos";'
    "let g = set_start {1, 2} of g;"
    "print (get_start g);"
    "let g = add_start {3} of g;"
    "print get_start g;"
)


def test_automaton2():
    res = interpret(program2)

    assert res == "{1, 2}\n{1, 2, 3}\n"
