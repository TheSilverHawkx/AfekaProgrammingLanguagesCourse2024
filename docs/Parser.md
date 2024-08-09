
# Parser

The parser takes the tokens produced by the lexer and arranges them into an Abstract Syntax Tree (AST) based on the BNF grammar of the language. The AST represents the hierarchical structure of the code, which is then analyzed and executed.

## BNF Grammar

The parser follows the BNF grammar defined in `BNF.txt`. This grammar specifies how different language constructs (like expressions, statements, and functions) are formed.

## Example

Given the tokens produced from `x + 2`, the parser would create an AST representing the addition of `x` and `2`.

