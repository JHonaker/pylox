import scanner

class Interpreter:

    def _evaluate(self, expr):
        return expr.accept(self)

    def _isTrue(obj):
        """Nil and false are false, everything else is true."""
        if obj is None:
            return False
        elif isinstance(obj, bool):
            return obj
        else:
            return True

    def _isEqual(left, right):
        if left is None:
            if right is None:
                return True
            else:
                return False
        else:
            return left == right

    def _concatOrAdd(left, right):
        if isinstance(left, Number) and isinstance(right, Number):
            return left + right
        elif isinstance(left, String) and isinstance(right, basestring):
            return left + right
        else:
            return None

    def visitLiteral(self, expr):
        return expr.value

    def visitGrouping(self, expr):
        return self._evaluate(expr.expression)

    def visitUnary(self, expr):
        right = self._evaluate(expr.right)

        result = {
            scanner.TokenType.MINUS : -right,
            scanner.TokenType.BANG  : not _isTrue(right)
        }.get(expr.operator.token_type)

        return result

    def visitBinary(self, expr):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        result = {
            scanner.TokenType.GREATER : lambda: left > right,
            scanner.TokenType.GREATER_EQUAL : lambda: left >= right,
            scanner.TokenType.LESS : lambda: left < right,
            scanner.TokenType.LESS_EQUAL : lambda: left <= right,
            scanner.TokenType.EQUAL_EQUAL : lambda: _isEqual(left, right),
            scanner.TokenType.BANG_EQUAL : lambda: not _isEqual(left, right),
            scanner.TokenType.MINUS : lambda: left - right,
            scanner.TokenType.PLUS : lambda: _concatOrAdd(left, right),
            scanner.TokenType.SLASH : lambda: left / right,
            scanner.TokenType.STAR : lambda: left * right
        }.get(expr.operator.token_type)

        return result


