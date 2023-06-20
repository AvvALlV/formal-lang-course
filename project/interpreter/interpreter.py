from Visitor import *
import sys


def interpreter(*argv):
    if len(argv[0]) == 0:
        sys.stdout.write("No file given, console mode is ON\n=====================\n")
        prog = "".join(sys.stdin.readlines())
    else:
        prog = read_program(Path(argv[0][0]))

    return _interpreter(prog)


def read_program(filename: Path) -> str:

    try:
        prog = filename.open()
    except FileNotFoundError as exception:
        raise RuntimeException(filename.name) from exception

    if not filename.name.endswith(".gql"):
        raise RuntimeException()

    return "".join(prog.readlines())


def _interpreter(prog: str):

    parser = parse(prog)
    tree = parser.program()

    if parser.getNumberOfSyntaxErrors() > 0:
        raise RuntimeException("Invalid syntax.")

    visitor = Visitor()
    visitor.visit(tree)

    return 0
