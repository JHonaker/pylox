#! /usr/local/bin/python3

import sys

def main():
    pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output directory>")
        sys.exit(1)

    main()
