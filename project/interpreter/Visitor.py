from collections import namedtuple
from typing import Any

from project.parser import *
from project.GQLanguageVisitor import *
from project.interpreter.Set import Set
from project.interpreter.FiniteAutomaton import FiniteAutomaton
from project.interpreter.Exceptions import *
from project.interpreter.Memory import Memory
from project.interpreter.Types import Type
from project.graph_utils import *
from project.finite_automaton import *
import sys

Lambda = namedtuple("lmda", ["args", "body"])


class Visitor(GQLanguageVisitor):
    _matched_val: Any

    def __init__(self, outStream=sys.stdout):
        self.memory = Memory()
        self.outStream = outStream
        self.memory.add_variable("True", True)
        self.memory.add_variable("False", False)

    def checkType(self, obj, expectedType):
        if not isinstance(obj, expectedType):
            raise TypingError(f"{type(obj)} is not a {expectedType}")

    def visitProgram(self, ctx: GQLanguageParser.ProgramContext):
        for stmt in ctx.stmt():
            stmt.accept(self)

    def visitIntLiteral(self, ctx: GQLanguageParser.IntLiteralContext):
        return int(str(ctx.INT().getText()))

    def visitStringLiteral(self, ctx: GQLanguageParser.StringLiteralContext):
        return str(ctx.STRING().getText()).strip('"')

    def visitEmptySet(self, ctx: GQLanguageParser.EmptySetContext):
        return Set(set())

    def visitNotEmptySet(self, ctx: GQLanguageParser.NotEmptySetContext):
        res_set = set()

        for el in ctx.elem():
            el = el.accept(self)
            res_set.update(el)
        return Set(res_set)

    def visitElSet(self, ctx: GQLanguageParser.ElSetContext):
        return ctx.el.accept(self)

    def visitRangeSet(self, ctx: GQLanguageParser.RangeSetContext):
        from_range = ctx.from_.accept(self)
        to_range = ctx.to.accept(self)
        return set(range(from_range, to_range + 1))

    def visitPrint(self, ctx: GQLanguageParser.PrintContext):
        value = ctx.value.accept(self)
        self.outStream.write(str(value) + "\n")

    def visitBind(self, ctx: GQLanguageParser.BindContext):
        name = ctx.name.accept(self)
        value = ctx.body.accept(self)

        self.memory.add_variable(name, value)

    def visitVarPattern(self, ctx: GQLanguageParser.VarPatternContext):
        return ctx.var().getText()

    def visitSetPattern(self, ctx: GQLanguageParser.SetPatternContext):
        pattern_context = {}

        for pattern in ctx.pattern():
            tmp_value = pattern.accpet(self)
            if tmp_value in pattern_context:
                raise RuntimeException("Same name args")

            pattern_context[pattern.accept(self)] = None
        return pattern_context

    def visitVal(self, ctx: GQLanguageParser.ValContext):
        return self.visitChildren(ctx)

    def visitVar(self, ctx: GQLanguageParser.VarContext):
        name = ctx.getText()
        return self.memory.find_variable(str(name))

    def applyLambda(self, lamb: Lambda, value: Type = None) -> Type:
        self.memory = self.memory.next_scope()

        if len(lamb.args) > 0 and value is not None:
            name = next(iter(lamb.args))
            self.memory.add_variable(name, value)

        result = lamb.body.accept(self)

        self.memory = self.memory.previous_scope()

        return result

    def visitLambdaParens(self, ctx: GQLanguageParser.LambdaParensContext):
        return ctx.internalLambda.accpet(self)

    def visitLambdaLiteral(self, ctx: GQLanguageParser.LambdaLiteralContext):
        args = ctx.args.accept(self)
        body = ctx.expr()
        return Lambda(args, body)

    def visitExprVar(self, ctx: GQLanguageParser.ExprVarContext):
        return ctx.var().accept(self)

    def visitExprSetStart(self, ctx: GQLanguageParser.ExprSetStartContext):
        start_states = ctx.states.accept(self)
        self.checkType(start_states, Set)

        fa = ctx.automaton.accept(self)
        self.checkType(fa, FiniteAutomaton)

        return fa.setStart(start_states)

    def visitExprSetFinal(self, ctx: GQLanguageParser.ExprSetFinalContext):
        final_states = ctx.states.accept(self)
        self.checkType(final_states, Set)

        fa = ctx.automaton.accept(self)
        self.checkType(fa, FiniteAutomaton)

        return fa.setFinal(final_states)

    def visitExprAddStart(self, ctx: GQLanguageParser.ExprAddStartContext):
        start_states = ctx.states.accept(self)
        self.checkType(start_states, Set)

        fa = ctx.automaton.accept(self)
        self.checkType(fa, FiniteAutomaton)
        return fa.addStart(start_states)

    def visitExprAddFinals(self, ctx: GQLanguageParser.ExprAddFinalsContext):
        final_states = ctx.states.accept(self)
        self.checkType(final_states, Set)

        fa = ctx.automaton.accept(self)
        self.checkType(fa, FiniteAutomaton)

        return fa.setFinal(final_states)

    def visitExprGetStart(self, ctx: GQLanguageParser.ExprGetStartContext):
        fa = ctx.automaton.accept(self)
        self.checkType(fa, FiniteAutomaton)
        return fa.start

    def visitExprGetFinal(self, ctx: GQLanguageParser.ExprGetFinalContext):
        fa = ctx.automaton.accept(self)
        self.checkType(fa, FiniteAutomaton)
        return fa.finals

    def visitExprGetVertices(self, ctx: GQLanguageParser.ExprGetVerticesContext):
        fa = ctx.automaton.accept(self)
        self.checkType(fa, FiniteAutomaton)
        return fa.vertices

    def visitExprGetEdges(self, ctx: GQLanguageParser.ExprGetEdgesContext):
        fa = ctx.automaton.accept(self)
        self.checkType(fa, FiniteAutomaton)
        return fa.edges

    def visitExprGetLabels(self, ctx: GQLanguageParser.ExprGetLabelsContext):
        fa = ctx.automaton.accept(self)
        self.checkType(fa, FiniteAutomaton)
        return fa.labels

    def visitExprGetReachable(self, ctx: GQLanguageParser.ExprValContext):
        fa = ctx.automaton.accept(self)
        self.checkType(fa, FiniteAutomaton)
        return fa.getReachable()

    def iterFunc(self, ctx, typeFunc: str = "map"):
        mset = ctx.usedSet.accept(self)
        self.checkType(mset, Set)

        func = ctx.func.accept(self)
        if len(mset) == 0:
            return Set(mset._set)

        new_set = set()
        for elem in mset._set:
            result = self.applyLambda(func, elem)
            if typeFunc == "map":
                new_set.add(result)
            elif typeFunc == "filter":
                if result:
                    new_set.add(elem)

        return Set(new_set)

    def visitExprMap(self, ctx: GQLanguageParser.ExprMapContext):
        return self.iterFunc(ctx, "map")

    def visitExprFilter(self, ctx: GQLanguageParser.ExprFilterContext):
        return self.iterFunc(ctx, "filter")

    def visitExprIntersect(self, ctx: GQLanguageParser.ExprIntersectContext):
        left = ctx.left.accept(self)
        right = ctx.right.accept(self)

        if type(left) == type(right) and isinstance(left, Type):
            return left.intersect(right)
        else:
            raise TypingError("Unknown type")

    def visitExprUnion(self, ctx: GQLanguageParser.ExprUnionContext):
        left = ctx.left.accept(self)
        right = ctx.right.accept(self)

        if type(left) == type(right) and isinstance(left, Type):
            return left.union(right)
        else:
            raise TypingError("Unknown type")

    def visitExprConcat(self, ctx: GQLanguageParser.ExprConcatContext):
        left = ctx.left.accept(self)
        right = ctx.right.accept(self)

        if type(left) == type(right) and isinstance(left, Type):
            return left.concatenate(right)
        else:
            raise TypingError("Unknown type")

    def visitExprClosure(self, ctx: GQLanguageParser.ExprKleeneContext):
        obj = ctx.first.accept(self)
        self.checkType(obj, FiniteAutomaton)

        return obj.kleene()

    def visitExprContains(self, ctx: GQLanguageParser.ExprContainsContext):
        left = ctx.left.accept(self)
        right = ctx.right.accept(self)
        self.checkType(right, Set)

        return right.find(left)

    def visitExprParens(self, ctx: GQLanguageParser.ExprParensContext):
        return ctx.internalExpr.accept(self)

    def visitExprSet(self, ctx: GQLanguageParser.ExprSetContext):
        expr_set = set()
        for expr in ctx.expr():
            expr_set.add(expr.accept(self))

        return Set(expr_set)

    def visitExprLoad(self, ctx: GQLanguageParser.ExprLoadContext):
        name = ctx.name.accept(self).strip('"')

        return FiniteAutomaton(graph_to_nfa(get_graph_by_name(name)))
