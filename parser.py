import grammar
import scanner

class ParseError(Exception):
      """Raise for an unexpected token in the parser."""

class Parser:

      def __init__(self, interpreter, token_list):

            self._interpreter = interpreter

            # The current head index in the token list
            self._current = 0

            self.token_list = token_list

      def parse(self):
            try:
                  return self._expression()
            except ParseError as error:
                  return None

      def _match(self, *token_types):
            """Looks ahead one token. If the next token matches one of the
            given ones, returns true and advances the head pointer."""
            for token in token_types:
                  if self._check(token):
                        self._advance()
                        return True

            return False

      def _check(self, token_type):
            """Checks the next token for the given token type."""
            if self._is_at_end():
                  return False

            return self._peek().token_type == token_type

      def _advance(self):
            """Advances the head pointer by one if not at the end.
            Always returns the previous token."""
            if not self._is_at_end():
                  self._current += 1
            return self._previous()

      def _is_at_end(self):
            """Returns True if the next token is an EOF."""
            return self._peek().token_type == scanner.TokenType.EOF

      def _peek(self):
            """Returns the token to be consumed next."""
            return self.token_list[self._current]

      def _previous(self):
            """Returns the previous token in the list."""
            return self.token_list[self._current - 1]

      def _expression(self):
            """Matches based on the rule:
            expression -> statement (, statement)*"""
            expr = self._statement()

            while self._match(scanner.TokenType.COMMA):
                  right = self._statement()
                  expr = grammar.Chain(expr, right)

            return expr

      def _statement(self):
            """Matches based on the rule:
            statement -> equality"""
            return self._equality()

      def _equality(self):
            """Matches based on the rule:
            equality -> comparison ( ( != | == ) comparison)*"""
            expr = self._comparison()

            # An Equality expression can match either a comparison
            # or comparison ((!= | ==) comparison)*
            while self._match(scanner.TokenType.BANG_EQUAL, scanner.TokenType.EQUAL_EQUAL):
                  operator = self._previous()
                  right = self._comparison()
                  expr = grammar.Binary(expr, operator, right)

            return expr

      def _comparison(self):
            """Matches based on the rule:
            comparison -> term ( ( > | >= | < | <= ) term)*"""
            expr = self._term()

            while self._match(scanner.TokenType.GREATER,
                              scanner.TokenType.GREATER_EQUAL,
                              scanner.TokenType.LESS,
                              scanner.TokenType.LESS_EQUAL):
                  operator = self._previous()
                  right = self._term()
                  expr = grammar.Binary(expr, operator, right)

            return expr

      def _term(self):
            """Matches based on the rule:
            term -> factor ( ( - | + ) factor)*"""
            expr = self._factor()

            while self._match(scanner.TokenType.MINUS, scanner.TokenType.PLUS):
                  operator = self._previous()
                  right = self._factor()
                  expr = grammar.Binary(expr, operator, right)

            return expr

      def _factor(self):
            """Matches based on the rule:
            factor -> unary ( ( / | * ) unary)*"""
            expr = self._unary()

            while self._match(scanner.TokenType.SLASH, scanner.TokenType.STAR):
                  operator = self._previous()
                  right = self._unary()
                  expr = grammar.Binary(expr, operator, right)

            return expr

      def _unary(self):
            """Matches based on the rule:
            unary -> ( ! | - ) unary
                   | primary"""
            if self._match(scanner.TokenType.BANG, scanner.TokenType.MINUS):
                  operator = self._previous()
                  right = self._unary()
                  return grammar.Unary(operator, right)

            return self._primary()

      def _primary(self):
            if self._match(scanner.TokenType.FALSE):
                  return grammar.Literal(False)
            elif self._match(scanner.TokenType.TRUE):
                  return grammar.Literal(True)
            elif self._match(scanner.TokenType.NIL):
                  return grammar.Literal(None)

            elif self._match(scanner.TokenType.NUMBER, scanner.TokenType.STRING):
                  return grammar.Literal(self._previous().literal)

            elif self._match(scanner.TokenType.LEFT_PAREN):
                  expr = self._expression()
                  self._consume(scanner.TokenType.RIGHT_PAREN,
                                "Expect ')' after expression.")
                  return grammar.Grouping(expr)

            raise self._error(self._peek(), "Expect expression.")

      def _consume(self, token_type, msg):
            """Attempts to consume the next token if it is the given type."""
            if self._check(token_type):
                  return self._advance()

            raise self._error(self._peek(), msg)

      def _error(self, token, msg):
            """Returns a ParseError and logs an error with the interpreter."""
            self._interpreter.parse_error(token, msg)
            return ParseError()

      def _synchronize(self):
            self._advance()

            while not self._is_at_end():
                  if self._previous().token_type == scanner.TokenType.SEMICOLON:
                        return

                  end_statement_tokens  = [scanner.TokenType.CLASS,
                                           scanner.TokenType.FUN,
                                           scanner.TokenType.VAR,
                                           scanner.TokenType.FOR,
                                           scanner.TokenType.IF,
                                           scanner.TokenType.WHILE,
                                           scanner.TokenType.PRINT,
                                           scanner.TokenType.RETURN]

                  if self._peek().token_type in end_statement_tokens:
                        return

                  self._advance()

