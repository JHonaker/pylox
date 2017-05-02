#! /usr/local/bin/python3

import grammar
import scanner

class AstPrinter:
    def printast(self, expr):
        return expr.accept(self)

    def visitBinary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGrouping(self, expr):
        return self.parenthesize("group", expr.expression)

    def visitLiteral(self, expr):
        return str(expr.value)

    def visitUnary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        string = "(" + name

        for expr in exprs:
            string += " "
            string += expr.accept(self)

        string += ")"

        return string

if __name__ == "__main__":
    expression = grammar.Binary(
        grammar.Unary(
            scanner.Token(scanner.TokenType.MINUS, "-", None, 1),
            Literal(123)),
        scanner.Token(scanner.TokenType.STAR, "*", None, 1),
        grammar.Grouping(
            grammar.Literal(45.67)))
    print(AstPrinter().printast(expression))
