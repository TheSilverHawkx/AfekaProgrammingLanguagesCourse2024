
# Symbol Table

The symbol table is an [Abstract Data Type (ADT)](https://en.wikipedia.org/wiki/Abstract_data_type) structure used by the semantic analyzer to store information about variables, functions, and lambda expressions within different scopes. Each scope has its own symbol table, allowing the interpreter to manage variable lifetimes and resolve identifiers correctly.

## Example

Continuing the example of the [semantic analyzer](./Semantic_Analyzer.md) file, here's our AST with the addition of symbol table illustration:

<div style="text-align: center;">
  <pre>
                                +-----------+                            +---------------------------------+
                                |  Program  |                            |            Symbol Table         |
                                +-----------+                            +---------------------------------+
                               /             \                           |  name | scope level |    type   |
                              /               \                          |       |             |           |
                             v                 v                         +-------+-------------+-----------+
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

When the sematic analyzer reaches the `FUNC_DECL` node it creates a new entry in the symbol table defining a function named `foo` like so:
<div style="text-align: center;">
  <pre>
                                +-----------+                            +---------------------------------+
                                |  Program  |                            |            Symbol Table         |
                                +-----------+                            +---------------------------------+
                               /             \                           |  name | scope level |    type   |
                              /               \                    *new* |  foo  |      1      |  function | *new*
                             v                 v                         +-------+-------------+-----------+
Semntic    +----------------+                  +-----------------+
Analyzer   |   FUNC_DECL    |                  |   FUNC_CALL     |
       ┗━> |      foo       |                  |      foo        |
           +----------------+                  +-----------------+
         /        |          \                  /              \
        v         v           v                v                v
   +--------+ +--------+ +-------------+   +--------+     +--------+
   | Param  | | Param  | | Expression  |   | Param  |     | Param  |
   |   x    | |   y    | |   x + y     |   |   1    |     |   2    |
   +--------+ +--------+ +-------------+   +--------+     +--------+

  </pre>
</div>

Then, when the sematic analyzer reaches the `FUNC_CALL` node, it looks up the name `foo` in the symbol table and check if it's of a function type:
<div style="text-align: center;">
  <pre>
                                +-----------+                            +---------------------------------+
                                |  Program  |                            |            Symbol Table         |
                                +-----------+                            +---------------------------------+
                               /             \                           |  name | scope level |    type   |
                              /               \                       => |  foo  |      1      |  function | <=
                             v                 v                         +-------+-------------+-----------+
Semntic    +----------------+                  +-----------------+          ▲
Analyzer   |   FUNC_DECL    |                  |   FUNC_CALL     |          ┃
       ┗━► |      foo       |                  |      foo        |  ◄━━━  Semntic
           +----------------+                  +-----------------+       Analyzer
         /        |          \                  /              \
        v         v           v                v                v
   +--------+ +--------+ +-------------+   +--------+     +--------+
   | Param  | | Param  | | Expression  |   | Param  |     | Param  |
   |   x    | |   y    | |   x + y     |   |   1    |     |   2    |
   +--------+ +--------+ +-------------+   +--------+     +--------+

  </pre>
</div>
