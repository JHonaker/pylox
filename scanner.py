import lox
from enum import Enum

TokenType = Enum(
    # Single character tokens
    LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE,
    COMMA, DOT, MINUS, PLUS, SEMICOLON, SLASH, STAR,

    # One or two character tokens
    BANG, BANG_EQUAL,
    EQUAL, EQUAL_EQUAL,
    GREATER, GREATER_EQUAL,
    LESS, LESS_EQUAL,

    # Literals
    IDENTIFIER, STRING, NUMBER,

    # Keywords
    AND, CLASS, ELSE, FALSE, FUN, FOR, IF, NIL, OR,
    PRINT, RETURN, SUPER, THIS, TRUE, VAR, WHILE,

    EOF
)

class Token:

    def __init__(token_type, lexeme, literal, line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__():
        return self.type + " " + lexeme + " " + literal


class Scanner:

    def __init__(source):
        """For the initialization of a scanner, we want a reference to
        the source material as well as an empty list of tokens."""
        self._source = source
        self._tokens = []

        # Indicies for current lexeme
        self._start = 0
        self._current = 0

    @property
    def tokens():
        return self._tokens

    def _at_eol(line):
        if self._current >= len(line):
            return True
        else:
            return False

    def scan_tokens():
        """Populate the internal token list given the source material."""
        for line_number, line in enumerate(self._source):
            self._scan_line(line, line_number)

        self._tokens.append(Token(TokenType.EOF, "",
                                  None, len(self._source) - 1))

        return self._tokens

    def _scan_line(line, line_number):
        self._start = 0
        self._current = 0
        while self._current < len(line):
            self._start = self._current
            self._scan_token(line, line_number)

    def _scan_token(line, line_number):
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

    def _advance(line):
        self._current = self._current + 1
        return line[self._current - 1]

    def _match(line, expected):
        if self._at_eol(line):
            return False

        if line[self._current] == expected:
            self._advance()
            return True
        else:
            return False

    def _peek(line):
        """Like advance, but does not consume the character."""
        if self._at_eol(line):
            return '\0'
        else:
            return line[self._current]

    def _consume_to(char, line):
        while self._peek() != char and self._at_eol():
            self._advance()
        return None

    def _consume_string(line):
        self._consume_to('"', line)

        if self._at_eol(line):
            lox.error(line, "Unterminated string.")
            return

        self._advance()

        return TokenType.STRING

    def _add_token(token_type, line, line_number, literal = None):
        text = line[start:(current + 1)]
        self._tokens.append(Token(token_type, text, literal, line_number))
