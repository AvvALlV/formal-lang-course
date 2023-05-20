from antlr4 import ParseTreeWalker, ParserRuleContext
from antlr4.error.Errors import ParseCancellationException
from antlr4.tree.Tree import TerminalNodeImpl
from pydot import Dot, Edge, Node
from antlr4 import InputStream, CommonTokenStream
from pathlib import Path
from project.GQLanguageLexer import GQLanguageLexer
from project.GQLanguageParser import GQLanguageParser
from project.GQLanguageListener import GQLanguageListener


def parse(text: str) -> GQLanguageParser:
    input_stream = InputStream(text)
    lexer = GQLanguageLexer(input_stream)
    lexer.removeErrorListeners()
    stream = CommonTokenStream(lexer)
    parser = GQLanguageParser(stream)

    return parser


def check_parser_correct(text: str) -> bool:
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.program()
    return parser.getNumberOfSyntaxErrors() == 0


def generate_dot(text: str, path: str):
    if not check_parser_correct(text):
        raise ParseCancellationException("The word doesn't match the grammar")
    ast = parse(text).program()
    tree = Dot("tree", graph_type="digraph")
    ParseTreeWalker().walk(DotTreeListener(tree, GQLanguageParser.ruleNames), ast)
    tree.write(str(path))


def generate_dot_str(text: str) -> str:
    if not check_parser_correct(text):
        raise ParseCancellationException("The word doesn't match the grammar")
    ast = parse(text).program()
    tree = Dot("tree", graph_type="digraph")
    ParseTreeWalker().walk(DotTreeListener(tree, GQLanguageParser.ruleNames), ast)
    return tree.to_string()


class DotTreeListener(GQLanguageListener):
    def __init__(self, tree: Dot, rules):
        self.tree = tree
        self.num_nodes = 0
        self.nodes = {}
        self.rules = rules
        super(DotTreeListener, self).__init__()

    def enterEveryRule(self, ctx: ParserRuleContext):
        if ctx not in self.nodes:
            self.num_nodes += 1
            self.nodes[ctx] = self.num_nodes
        if ctx.parentCtx:
            self.tree.add_edge(Edge(self.nodes[ctx.parentCtx], self.nodes[ctx]))
        label = self.rules[ctx.getRuleIndex()]
        self.tree.add_node(Node(self.nodes[ctx], label=label))

    def visitTerminal(self, node: TerminalNodeImpl):
        self.num_nodes += 1
        self.tree.add_edge(Edge(self.nodes[node.parentCtx], self.num_nodes))
        self.tree.add_node(Node(self.num_nodes, label=f"TERM: {node.getText()}"))
