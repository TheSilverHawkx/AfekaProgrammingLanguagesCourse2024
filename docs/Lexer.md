
# Lexer

The lexer is responsible for converting the input text into a series of tokens. Each token represents a meaningful sequence of characters (such as keywords, identifiers, operators, etc.) that the parser will use to build the Abstract Syntax Tree (AST).

## Token Types

Tokens are classified into different types, defined in the `token.py` module. These include types like `IDENTIFIER`, `NUMBER`, `OPERATOR`, and so on.

## Example

In the example below, we can see the tokens sequence generated from the input `( 1 + 2) * 5`:
```
                                              +-----------------+
                                              | "( 1 + 2 ) * 5" |
                                              +-----------------+
+--------+    +---------------+    +------+    +---------------+    +--------+    +-------+    +---------------+
| LPAREN | -> | CONST_INTEGER | -> | PLUS | -> | CONST_INTEGER | -> | RPAREN | -> | MULT  | -> | CONST_INTEGER |
+--------+    +---------------+    +------+    +---------------+    +--------+    +-------+    +---------------+
```
