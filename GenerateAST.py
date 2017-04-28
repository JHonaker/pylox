#! /usr/local/bin/python3

import sys

output_dir = None

tab = "    " # Tab is four spaces

base_desc = {
    "Expr": {
        "Unary": [["Token", "operator"], ["Expr", "right"]],
        "Binary": [["Expr", "left"], ["Token", "operator"], ["Expr", "right"]],
        "Grouping" : [["Expr", "expression"]],
        "Literal" : [["object", "value"]]
    }
}


def defineAst(base_name, types):
    path = output_dir + "/" + base_name + ".py"


    with open(path, "w+") as con:
        con.write("from scanner import Token\n\n\n")
        con.writelines(["class " + base_name + ":\n",
                        tab + "pass\n\n"])
        for expr_type, expr in types.items():
            defineType(con, base_name, expr_type, expr)

def defineType(con, base_name, class_name, fields):

    types, names = zip(*fields)

    field_str = ", ".join(names)

    assert_stmts = [tab + tab +
                    "assert isinstance(" + field[1] + ", " + field[0] + ")\n"
                    for field in fields]

    var_stmts = [tab + tab +
                 "self." + name + " = " + name + "\n"
                 for name in names]

    con.write("\n")
    con.writelines(["class " + class_name + "(" + base_name + "):\n"
                    "",
                    # The constructor
                    tab + "def __init__(self, " +field_str + "):\n"])
    con.writelines(assert_stmts)
    con.write("\n")
    con.writelines(var_stmts)
    con.write("\n")
    con.writelines([tab + "def accept(self, visitor):\n",
                    tab + tab + "return visitor.visit" + class_name + "(self)\n\n"])





if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output directory>")
        sys.exit(1)

    output_dir = sys.argv[1]
    defineAst("Expr", base_desc["Expr"])
