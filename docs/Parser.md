
# Parser

The parser takes the tokens produced by the lexer and arranges them into an Abstract Syntax Tree (AST) based on the BNF grammar of the language. The AST represents the hierarchical structure of the code, which is then analyzed and executed.

## BNF Grammar

The parser follows the BNF grammar defined in `BNF.txt`. This grammar specifies how different language constructs (like expressions, statements, and functions) are formed.

## Example

Given the tokens produced from `(1 + 2) * 5`, the parser would create an AST representing both the addition of `1` and `2`, and also its multiplication by `5`:

<div style="text-align: center;">
<pre>
                                          +-----------+
                                          |  Program  |
                                          +-----------+
                                               |
                                               v
                                          +-----------+
                                          |   BinOp   |
                                          |     *     |
                                          +-----------+
                                        /               \
                                       /                 \
                                      v                   v
                        +-----------+                     +-----------------+
                        |   BinOp   |                     |  CONST_INTEGER  |
                        |    +      |                     |        5        |
                        +-----------+                     +-----------------+
                       /             \          
                      v               v
        +---------------+           +---------------+
        | CONST_INTEGER |           | CONST_INTEGER |
        |       1       |           |       2       |
        +---------------+           +---------------+
</pre>
</div>
