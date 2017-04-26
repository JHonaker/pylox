import lox
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

    @property
    def tokens(self):
        return self._tokens

    def _at_eol(self, line):
        if self._current >= len(line):
            return True
        else:
            return False

    def scan_tokens(self):
        """Populate the internal token list given the source material."""
        for line_number, line in enumerate(self._source):
            self._scan_line(line, line_number)

        self._tokens.append(Token(TokenType.EOF, "",
                                  None, len(self._source) - 1))

        return self._tokens

    def _scan_line(self, line, line_number):
        self._start = 0
        self._current = 0
        while self._current < len(line):
            self._start = self._current
            self._scan_token(line, line_number)

    def _scan_token(self, line, line_number):
        char = self._advance(line)

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
            '/': lambda c: self._consume_to('\n', line) if self._match('/') else TokenType.SLASH,
            # Ignore Whitespace
            ' ':  lambda c: None,
            '\r': lambda c: None,
            '\t': lambda c: None,
            # Differs from Bob's since line_number comes from array index
            '\n': lambda c: None,
            # Strings consume to EOL or closing "
            '"': lambda c: self._consume_string(line)
        }

        if char in token_strings:
            token_type = token_strings[char](char)
            if token_type is not None:
                if token_type == TokenType.STRING:
                    string_literal = line[(self._start+1):self._current]
                    self._add_token(TokenType.STRING,
                                    line,
                                    line_number,
                                    string_literal)
                else:
                    self._add_token(token_strings[char](char),
                                    line,
                                    line_number)
            # Else it is a comment, and we don't want to add a token
        else:
            lox.error(line_number, "Unexpected character.")

    def _advance(self, line):
        self._current = self._current + 1
        return line[self._current - 1]

    def _match(self, line, expected):
        if self._at_eol(line):
            return False

        if line[self._current] == expected:
            self._advance()
            return True
        else:
            return False

    def _peek(self, line):
        """Like advance, but does not consume the character."""
        if self._at_eol(line):
            return '\0'
        else:
            return line[self._current]

    def _consume_to(self, char, line):
        while self._peek() != char and self._at_eol():
            self._advance()
        return None

    def _consume_string(self, line):
        self._consume_to('"', line)

        if self._at_eol(line):
            lox.error(line, "Unterminated string.")
            return

        self._advance()

        return TokenType.STRING

    def _add_token(self, token_type, line, line_number, literal = None):
        text = line[self._start:(self._current + 1)]
        self._tokens.append(Token(token_type, text, literal, line_number))
