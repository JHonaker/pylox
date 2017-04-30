import lox
import pdb
from enum import Enum

class TokenType(Enum):
    # Single character tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()


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
        self.tokens = []

        # Dictionary for lookup up token literals
        self._token_strings = {
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
            '/': lambda c: self._slash_logic(),
            # Ignore Whitespace
            ' ':  lambda c: None,
            '\r': lambda c: None,
            '\t': lambda c: None,
            # Differs from Bob's since line_number comes from array index
            '\n': lambda c: self._advance_line(),
            # Strings consume to EOL or closing "
            '"': lambda c: self._consume_string()
        }

        # Dictionary for lookup of reserved words
        self._reserved_strings = {
            "and":   TokenType.AND,
            "class": TokenType.CLASS,
            "else":  TokenType.ELSE,
            "false": TokenType.FALSE,
            "for":   TokenType.FOR,
            "fun":   TokenType.FUN,
            "if":    TokenType.IF,
            "nil":   TokenType.NIL,
            "or":    TokenType.OR,
            "print": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this":  TokenType.THIS,
            "true":  TokenType.TRUE,
            "var":   TokenType.VAR,
            "while": TokenType.WHILE
        }

        # Indicies for current lexeme
        self._start = 0
        self._current = 0
        self._line = 0


    def _at_eof(self, offset = 0):
        return self._current + offset >= len(self._source)

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


        if char in self._token_strings:
            token_type = self._token_strings[char](char)
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
            elif self._is_valid_literal_start_character(char):
                self._consume_identifier()
                token_type = self._recognize_reserved_words()
                self._add_token(token_type)
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
            if self._peek() == '\n':
                self._advance_line()
            self._advance()

        if self._at_eof():
            lox.error(self._line, "Unterminated string.")
            return

        self._advance()

        return TokenType.STRING

    def _consume_number(self):
        while self._peek().isdigit():
            self._advance()

        # Only consume a trailing period if it is followed by a digit
        if self._peek() == '.' and self._peek(2).isdigit():
            self._advance()

            while self._peek().isdigit():
                self._advance()

    def _consume_identifier(self):
        while self._is_valid_literal_character(self._peek()):
            self._advance()

    def _recognize_reserved_words(self):
        string = self._source[self._start:self._current]
        token_type = self._reserved_strings.get(string, None)

        if token_type is None:
            token_type = TokenType.IDENTIFIER

        return token_type

    def _is_valid_literal_start_character(self, c):
        return c.isalpha() or c == '_'

    def _is_valid_literal_character(self, c):
        return self._is_valid_literal_start_character(c) or c.isdigit()

    def _advance_line(self):
        self._line = self._line + 1

    def _add_token(self, token_type, literal = None):
        text = self._source[self._start:self._current]
        self._tokens.append(Token(token_type, text, literal, self._line))

    def _slash_logic(self):
        if self._match('/'):
            self._consume_to('\n')

        elif self._match('*'):
            while self._peek() != '*' and self._peek(2) != '/' and not self._at_eof():
                if self._peek() == '\n':
                    self._advance_line()
                self._advance()

            if self._at_eof():
                lox.error(self._line, "Unterminated comment.")
                return None

            # Consume '*/'
            self._advance()
            self._advance()

        else:
            return TokenType.SLASH
