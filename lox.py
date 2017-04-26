#!/usr/local/bin/python3

import sys
import scanner as scn

had_error = False

def run_file(path):
    file = open(path, "r")
    lines = file.readlines()
    file.close()

    run(lines)

    if had_error:
        sys.exit(65)

def run_prompt():
    while True:
        line = input("pylox> ")
        run(line)

        # If we had an error, we should reset at new prompt
        had_error = False

def run(source):
    scanner = scn.Scanner(source)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(token)


def error(line, msg):
    report(line, "", msg)

def report(line, where, msg):
    print("[line " + line + "] Error" + where + ": " + msg)
    had_error = True


# The main insertion point for the interpreter
def main():
    # The first argument in sys.argv will alwyas be lox.py
    num_args = len(sys.argv) - 1
    if num_args > 1:
        print("Usage: pylox [script]")
    elif num_args == 1:
        run_file(sys.argv[1])
    else:
        run_prompt()

if __name__ == "__main__":
    main()
