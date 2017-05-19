import numbers
import scanner

class LoxRuntimeError(Exception):
    """Raise when the Lox interpreter encounters a runtime error."""
    def __init__(self, token, message):
        self.message = message
        self.token = token


def _stringify(obj):
    if obj is None:
        return "nil"
    else:
        return str(obj)

def _isTrue(obj):
    """Nil and false are false, everything else is true."""
    if obj is None:
        return False
    elif isinstance(obj, bool):
        return bool(obj)
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

def _concatOrAdd(operator, left, right):
    if isinstance(left, numbers.Number) and isinstance(right, numbers.Number):
        return float(left) + float(right)
    elif isinstance(left, str) and isinstance(right, str):
        return left + right
    else:
        raise LoxRuntimeError(operator, "Operands must be two numbers or two strings.")

def _checkNumberOperand(operator, operand):
    if isinstance(operand, numbers.Number):
        return

    raise LoxRuntimeError(operator, "Operand must be a number.")

def _checkNumberOperands(operator, left, right):
    if isinstance(left, numbers.Number) and isinstance(right, numbers.Number):
        return
    raise LoxRuntimeError(operator, "Operands must be numbers.")


class Interpreter:

    def __init__(self, lox):
        self._lox = lox

    def interpret(self, expression):
        try:
            value = self._evaluate(expression)
            print(_stringify(value))
        except LoxRuntimeError as error:
            self._lox.runtime_error(error)

    def _evaluate(self, expr):
        return expr.accept(self)



    def visitLiteral(self, expr):
        return expr.value

    def visitGrouping(self, expr):
        return self._evaluate(expr.expression)

    def visitUnary(self, expr):
        right = self._evaluate(expr.right)

        op_type = expr.operator.token_type

        if op_type is scanner.TokenType.MINUS:
            _checkNumberOperand(expr.operator, right)
            return -float(right)
        elif op_type is scanner.TokenType.BANG :
            return isTrue(right)

        return None

    def visitBinary(self, expr):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        op_type = expr.operator.token_type

        if op_type is scanner.TokenType.GREATER:
            _checkNumberOperands(expr.operator, left, right)
            return float(left) >= float(right)

        elif op_type is scanner.TokenType.GREATER:
            _checkNumberOperands(expr.operator, left, right)
            return float(left) >= float(right)

        elif op_type is scanner.TokenType.LESS:
            _checkNumberOperands(expr.operator, left, right)
            return float(left) < float(right)

        elif op_type is scanner.TokenType.LESS_EQUAL:
            _checkNumberOperands(expr.operator, left, right)
            return float(left) <= float(right)

        elif op_type is scanner.TokenType.EQUAL_EQUAL:
            return _isEqual(left, right)

        elif op_type is scanner.TokenType.BANG_EQUAL:
            return not _isEqual(left, right)

        elif op_type is scanner.TokenType.MINUS:
            _checkNumberOperands(expr.operator, left, right)
            return float(left) - float(right)

        elif op_type is scanner.TokenType.PLUS:
            return _concatOrAdd(expr.operator, left, right)

        elif op_type is scanner.TokenType.SLASH:
            _checkNumberOperands(expr.operator, left, right)
            return float(left) / float(right)

        elif op_type is scanner.TokenType.STAR:
            _checkNumberOperands(expr.operator, left, right)
            return float(left) * float(right)

        return None


