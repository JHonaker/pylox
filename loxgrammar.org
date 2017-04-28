* Lox Grammar

** Literals
   - Numbers
   - Strings
   - Booleans
   - nil

** Unary Expressions
   - Prefix ! (logical not)
   - `-` to negate a number

** Binary Expressions
   - Infix arithmetic (`+`, `-`, `*`, `/`)
   - Logic operators (`!=`, `<`, `<=`, `>`, `>=`)
 
** Parentheses for grouping

* Grammar for Above Subset

#+BEGIN_EXAMPLE
expression -> literal
           |  unary
           |  binary
           |  grouping

literal    -> NUMBER | STRING | "true" | "false" | "nil"
grouping   -> "(" expression ")"
unary      -> ( "-" | "!" ) expression
binary     -> expression operator expression
operator   -> "==" | "!+" | "<" | "<=" | ">" | ">="
           |  "+"  | "-"  | "*" | "/"
#+END_EXAMPLE
