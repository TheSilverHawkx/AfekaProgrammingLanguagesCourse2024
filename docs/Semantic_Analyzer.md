
# Semantic Analyzer

The semantic analyzer performs checks on the AST produced by the [parser](./Parser.md) to ensure that the code is [semantically correct](https://en.wikipedia.org/wiki/Semantic_analysis_(linguistics)). This includes scope checking, type checking, and ensuring that variables are declared before they are used.

The analyzer traverses the AST and checks for any semantic errors that could cause the code to behave unexpectedly at runtime.

In this language, there are no assignment operations and types are infferred during execution and so the semantic analyer's main purpose is to verify functions were defined before execution.

## Example

Let's take a look at the AST tree for the following code:
```
Defun {'name' : 'foo', 'arguments': (x,y)}
  x + y

foo(1,2)
```

Its AST will look like this:
<div style="text-align: center;">
  <pre>
                                +-----------+
                                |  Program  |
                                +-----------+
                               /             \
                              /               \
                             v                 v
           +----------------+                  +-----------------+
           |   FUNC_DECL    |                  |   FUNC_CALL     |
           |      foo       |                  |      foo        |
           +----------------+                  +-----------------+
         /        |          \                  /              \
        v         v           v                v                v
   +--------+ +--------+ +-------------+   +--------+     +--------+
   | Param  | | Param  | | Expression  |   | Param  |     | Param  |
   |   x    | |   y    | |   x + y     |   |   1    |     |   2    |
   +--------+ +--------+ +-------------+   +--------+     +--------+

  </pre>
</div>

By following the PreOrder Traversal method, the semantic analyzer will first reach the `FUNC_DECL` node and define the `foo` function within its [symbols table](./Symbol_Table.md).
It will then go to the `FUNC_CALL` node and check said symbols table for a function named `foo`.

Since `FUNC_DECL` happened before `FUNC_CALL` - the symbols table already has a reference for the `foo` function and thus not throw a semantic error.

Had we switched the order of statments in our code to: function call first - the `FUNC_CALL` node would've been on the left of the `Program`.

By the time the semantic analyzer reached the `FUNC_CALL` node, the `foo` function was not yet added to the symbols table - meaning it was not defined yet, and thus throw a semantic error.
