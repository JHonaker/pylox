from scanner import TokenType, Token
import grammar


class Parser:

      def __init__(self, token_list):

            # The current head index in the token list
            self._current = 0

            self.token_list = token_list

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
            return self._peek().token_type == TokenType.EOF

      def _peek(self):
            """Returns the token to be consumed next."""
            return self.token_list[self._current]

      def _previous(self):
            """Returns the previous token in the list."""
            return self._token_list[self._current - 1]

      def _expression(self):
            """Matches based on the rule:
            expression -> equality"""
            return self._equality()

      def _equality(self):
            """Matches based on the rule:
            equality -> comparison ( ( != | == ) comparison)*"""
            expr = self._comparison()

            # An Equality expression can match either a comparison
            # or comparison ((!= | ==) comparison)*
            while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
                  operator = self._previous()
                  right = self._comparison()
                  expr = grammer.Binary(expr, operator, right)

            return expr
