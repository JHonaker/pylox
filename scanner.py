import lox
import pdb
from enum import Enum

class TokenType(Enum):
    # Single character tokens
    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    COMMA = 5
    DOT = 6
    MINUS = 7
    PLUS = 8
    SEMICOLON = 9
    SLASH = 10
    STAR = 11

    # One or two character tokens
    BANG = 12
    BANG_EQUAL = 13
    EQUAL = 14
    EQUAL_EQUAL = 15
    GREATER = 16
    GREATER_EQUAL = 17
    LESS = 18
    LESS_EQUAL = 19

    # Literals
    IDENTIFIER = 20
    STRING = 21
    NUMBER = 22

    # Keywords
    AND = 23
    CLASS = 24
    ELSE = 25
    FALSE = 26
    FUN = 27
    FOR = 28
    IF = 29
    NIL = 30
    OR = 31
    PRINT = 32
    RETURN = 33
    SUPER = 34
    THIS = 35
    TRUE = 36
    VAR = 37
    WHILE = 38

    EOF = 39


class Token:

    def __init__(self, token_type, lexeme, literal, line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return str(self.token_type) + " " + str(self.lexeme) + " " + str(self.literal)


class Scanner:

    def __init__(self, source):
        """For the initialization of a scanner, we want a reference to
        the source material as well as an empty list of tokens."""
        self._source = source
        self._tokens = []

        # Indicies for current lexeme
        self._start = 0
        self._current = 0
        self._line = 0

    @property
    def tokens(self):
        return self._tokens

    def _at_eof(self):
        return self._current >= len(self._source)

    def scan_tokens(self):
        """Populate the internal token list given the source material."""
        while not self._at_eof():
            self._start = self._current
            self._scan_token()

        self._tokens.append(Token(TokenType.EOF, "",
                                  None, len(self._source) - 1))

        return self._tokens

    def _scan_token(self):
        char = self._advance()

        token_strings = {
            # Single character tokens
            '(': lambda c: TokenType.LEFT_PAREN,
            ')': lambda c: TokenType.RIGHT_PAREN,
            '{': lambda c: TokenType.LEFT_BRACE,
            '}': lambda c: TokenType.RIGHT_BRACE,
            ',': lambda c: TokenType.COMMA,
            '.': lambda c: TokenType.DOT,
            '-': lambda c: TokenType.MINUS,
            '+': lambda c: TokenType.PLUS,
            ';': lambda c: TokenType.SEMICOLON,
            '*': lambda c: TokenType.STAR,
            # Look ahead one to match the 1 or 2 character tokens
            '!': lambda c: TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG,
            '=': lambda c: TokenType.EQUAL_EQUAL if self._match('=') else TokenType.EQUAL,
            '<': lambda c: TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS,
            '>': lambda c: TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER,
            '/': lambda c: self._consume_to('\n') if self._match('/') else TokenType.SLASH,
            # Ignore Whitespace
            ' ':  lambda c: None,
            '\r': lambda c: None,
            '\t': lambda c: None,
            # Differs from Bob's since line_number comes from array index
            '\n': lambda c: self._advance_line(),
            # Strings consume to EOL or closing "
            '"': lambda c: self._consume_string()
        }

        if char in token_strings:
            token_type = token_strings[char](char)
            if token_type is not None:
                if token_type == TokenType.STRING:
                    string_literal = self._source[(self._start+1):(self._current - 1)]
                    self._add_token(TokenType.STRING, string_literal)
                else:
                    self._add_token(token_type)
            # Else it is a comment, and we don't want to add a token
        else:
            if char.isdigit():
                self._consume_number()
                number_string = self._source[self._start:self._current]
                number_literal = float(number_string) if '.' in number_string else int(number_string)
                self._add_token(TokenType.NUMBER, number_literal)
            else:
                lox.error(self._line, "Unexpected character.")

    def _advance(self):
        self._current = self._current + 1
        return self._source[self._current - 1]

    def _match(self, expected):
        if self._at_eof():
            return False

        if self._source[self._current] == expected:
            self._advance()
            return True
        else:
            return False

    def _peek(self, ahead = 1):
        """Like advance, but does not consume the character."""
        offset = ahead - 1
        if self._at_eof(offset):
            return '\0'
        else:
            return self._source[self._current + offset]

    def _consume_to(self, char):
        while self._peek() != char and not self._at_eof():
            self._advance()
        return None

    def _consume_string(self):
        while self._peek() != '"' and not self._at_eof():
            if self._peek == '\n':
                self._line = self._line + 1
            self._advance()

        if self._at_eof():
            lox.error(self._line, "Unterminated string.")
            return

        self._advance()

        return TokenType.STRING

    def _advance_line(self):
        self._line = self._line + 1

    def _add_token(self, token_type, literal = None):
        text = self._source[self._start:self._current]
        self._tokens.append(Token(token_type, text, literal, self._line))
