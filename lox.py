#!/usr/local/bin/python3

import sys
import scanner as scn
import parser as prs
import interpreter as interp
import astprinter

class lox:

    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

        self.interpreter = interp.Interpreter(self)

    def run_file(self, path):
        file = open(path, "r")
        source = file.read()
        file.close()

        self.run(source)

        if self.had_error:
            sys.exit(65)
        elif self.had_runtime_error:
            sys.exit(70)

    def run_prompt(self):
        while True:
            line = input("pylox> ")
            self.run(line)

            # If we had an error, we should reset at new prompt
            self.had_error = False
            self.had_runtime_error = False

    def run(self, source):
        scanner = scn.Scanner(self, source)
        tokens = scanner.scan_tokens()
        parser = prs.Parser(self, tokens)
        expression = parser.parse()

        self.interpreter.interpret(expression)

    def parse_error(self, token, msg):
        if token.token_type == scn.TokenType.EOF:
            self.report(token.line, "at end", msg)
        else:
            self.report(token.line, " at '" + token.lexeme + "'", msg )

    def scan_error(self, line, msg):
        self.report(line, "", msg)

    def runtime_error(self, error):
        print(error.message, "\n[line ", error.token.line, "]")
        self.had_runtime_error = True

    def report(self, line, where, msg):
        print("[line " + str(line) + "] Error" + str(where) + ": " + str(msg))
        self.had_error = True


# The main insertion point for the program
def main():
    program = lox()
    # The first argument in sys.argv will alwyas be lox.py
    num_args = len(sys.argv) - 1
    if num_args > 1:
        print("Usage: pylox [script]")
    elif num_args == 1:
        program.run_file(sys.argv[1])
    else:
        program.run_prompt()

if __name__ == "__main__":
    main()
