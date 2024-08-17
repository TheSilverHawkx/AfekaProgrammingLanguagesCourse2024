# BNF Grammar for Custom Language

## Grammar Structure

This document provides a detailed description of the Backus-Naur Form (BNF) grammar of the programming language.

### Production Rules

```bnf
<program> ::= <statement_list>
<statement_list> ::= <statement> | <statement> <statement_list>

<statement> ::= <empty>
              | <function_declaration>
              | <logical_expr> 
              | "(" <statement> ")"

<lambda_decleration> ::= "(" "Lambd" <formal_parameters> "." <logical_expr> ")"
                       | "(" "Lambd" <formal_parameters> "." <lambda_decleration> ")"

<nested_lambda> ::= <lambda_decleration> "(" <actual_parameters> ")"

<function_declaration> ::= "Defun" "{" <function_conf_name> "," <function_conf_args> "}" <logical_expr>
                         | "Defun" "{" <function_conf_args> "," <function_conf_name> "}" <logical_expr>

<function_conf_name> ::= "'" "name" "'" ":" "'" <identifier> "'"
<function_conf_args> ::= "'" "arguments" "'" ":" "(" <formal_parameters> ")"

<formal_parameters> ::= <identifier>
                      | <identifier> ','
                      | <identifier> ',' <formal_parameters>


<logical_expr>  ::= <compare_expr> | <compare_expr> <binary_op> <logical_expr>
<compare_expr>  ::= <addition_expr> | <addition_expr> <compare_op> <addition_expr>
<addition_expr> ::= <multiplication_expr> | <multiplication_expr> <addition_op> <addition_expr>
<multiplication_expr> ::= <factor> | <factor> <mult_op> <multiplication_expr>
<factor> ::= <integer>
           | <boolean>
           | <function_call>
           | <identifier>
           | "(" <logical_expr> ")"
           | "!" <logical_expr>
           | "not" <logical_expr>
           | <addition_op> <factor>
           | <nested_lambda>

<function_call> ::= <identifier> "(" <actual_parameters> ")"
<actual_parameters> ::= <logical_expr>
                      | <logical_expr> ","
                      | <logical_expr> "," <actual_parameters>
                      | <empty>
                      | <lambda_decleration> ","  <actual_parameters>
                      | <lambda_decleration> ","
                      | <lambda_decleration>


<integer>       ::= <digit> | <digit> <integer>
<identifier>    ::= <character>
                  | <character> <identifier>
                  | <identifier> <digit>
                  | <identifier> <digit> <identifier>
<boolean>       ::= "True" | "False"
<binary_op>     ::= "&&" | "||" | "or" | "and"
<compare_op>    ::= "==" | "!=" | ">" | "<" | ">=" | "<="
<addition_op>   ::= "+"  | "-" 
<mult_op>       ::= "*" | "/" | "%"
<character>     ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z"
<digit>         ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<empty>         ::=
```
Symbol Structure
--
### Program
**`<program>`**: Represents the entire program, and is the root of the whole program.
  ```bnf
  <program> ::= <statement_list>
  ```

### Statement List
**`<statement_list>`**: A sequence of statements.
  ```bnf
  <statement_list> ::= <statement> | <statement> <statement_list>
  ```

### Statements
**`<statement>`**: Represents the different types of executable instructions within the program.
  ```bnf
  <statement> ::= <empty>
              | <function_declaration>
              | <logical_expr> 
              | "(" <statement> ")"
  ```

### Lambda
* **`<lambda_decleration>`**: Defines an anonymous  function (lambda) with parameters and an expression or a declaration
  ```bnf
  <lambda_decleration> ::= "(" "Lambd" <formal_parameters> "." <logical_expr> ")"
  ```
* **`<nested_lambda>`**: Defined an anonymous  function and it's call within another a statement.
  ```bnf
  <nested_lambda> ::= <lambda_decleration> "(" <actual_parameters> ")"
  ```

### Function Declaration
- **`<function_declaration>`**: Defines a named function with arguments and a body expression.
The order of the function's configuration is dynamic.
  ```bnf
  <function_declaration> ::= "Defun" "{" <function_conf_name> "," <function_conf_args> "}" <logical_expr>
                           | "Defun" "{" <function_conf_args> "," <function_conf_name> "}" <logical_expr>
  ```

- **`<function_conf_name>`**: Specifies the name of the function.
  ```bnf
  <function_conf_name> ::= "'" "name" "'" ":" "'" ID "'"
  ```

- **`<function_conf_args>`**: Specifies the arguments of the function.
  ```bnf
  <function_conf_args> ::= "'" "arguments" "'" ":" "(" <formal_parameters> ")"
  ```

### Formal Parameter List
**`<formal_parameters>`**: Defines the list of parameters for a function.
The symbol has multiple productions to account for the optional positioning of a comma (`,`) after the last parameter.
  ```bnf
  <formal_parameters> ::= <identifier> | <identifier> ',' | <identifier> ',' <formal_parameters>
  ```

### Logical Expressions
**`<logical_expr>`**: Represents a logical binary operation (`AND`,`OR`), or a comparison operation
  ```bnf
  <logical_expr>  ::= <compare_expr> | <compare_expr> <binary_op> <logical_expr>
  ```

### Comparison Expressions
**`<compare_expr>`**: Represents a comparison binary operation (`==`,`>`,`<`, etc.), or an addition arithmetic operation.

Note: 
  ```bnf
  <compare_expr>  ::= <addition_expr> | <addition_expr> <compare_op> <addition_expr>
  ```

### Additive Expressions
**`<addition_expr>`**: Represents an binary addition arithmetic operation (`+`, `-`), or a multiplication operation.
Note: The addition symbol encapsulates the multiplication symbol in order to implement PEMDAS rules.
  ```bnf
  <addition_expr> ::= <multiplication_expr> | <multiplication_expr> <addition_op> <addition_expr>
  ```

### Multiplicative Expressions
**`<multiplication_expr>`**: Represents a binary multiplication operation (`*`,`/`,`%`), a unary operation (`-`,`+`,`!`), or a terminal value.
Note: The multiplication symbol encapsulates unary operation symbols to implement PEMDAS rules.
  ```bnf
  <multiplication_expr> ::= <factor> | <factor> <mult_op> <multiplication_expr>
  ```

### Factors
**`<factor>`**: Represents the basic elements in an expression, including integers, booleans, function calls, and identifiers.
In addition this symbol also include the unary operations (`-`,`+`,`!`).
Note: parenthesis encapsulation is also implemented here to implement PEMDAS rules.
  ```bnf
  <factor> ::= <integer>
             | <boolean>
             | <function_call>
             | <identifier>
             | "(" <logical_expr> ")"
             | "!" <logical_expr>
             | "not" <logical_expr>
             | <addition_op> <factor>
  ```

### Function Call
- **`<function_call>`**: Represents a call to a function with parameters.
  ```bnf
  <function_call> ::= <identifier> "(" <actual_parameters> ")"
  ```

- **`<actual_parameters>`**: The parameters passed to a function call.
  ```bnf
  <actual_parameters> ::= <logical_expr>
                      | <logical_expr> ","
                      | <logical_expr> "," <actual_parameters>
                      | <empty>
                      | <lambda_decleration> ","  <actual_parameters>
                      | <lambda_decleration> ","
                      | <lambda_decleration>
  ```

### Terminal Symbols

- **`<integer>`**: A whole integer value defined as a digit or a sequence of digits.
  ```bnf
  <integer> ::= <digit> | <digit> <integer>
  ```

- **`<identifier>`**: A name or a reserved keyword, made up of characters and digits.
  ```bnf
  <identifier> ::= <character>
                 | <character> <identifier>
                 | <identifier> <digit>
                 | <identifier> <digit> <identifier>
  ```

- **`<boolean>`**: Represents a boolean value.
  ```bnf
  <boolean> ::= "True" | "False"
  ```

- **`<binary_op>`**: Logical operators for combining boolean expressions.
  ```bnf
  <binary_op> ::= "&&" | "||" | "or" | "and"
  ```

- **`<compare_op>`**: Operators for comparing values.
  ```bnf
  <compare_op> ::= "==" | "!=" | ">" | "<" | ">=" | "<="
  ```

- **`<addition_op>`**: Operators for addition and subtraction.
  ```bnf
  <addition_op> ::= "+"  | "-" 
  ```

- **`<mult_op>`**: Operators for multiplication, division, and modulus.
  ```bnf
  <mult_op> ::= "*" | "/" | "%"
  ```

- **`<character>`**: A single alphabetical character.
  ```bnf
  <character> ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z"
  ```

- **`<digit>`**: A single numeric digit.
  ```bnf
  <digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
  ```

- **`<empty>`**: Represents an empty production.
  ```bnf
  <empty> ::=
  ```
  
## Limitations of the Language

1. **Lack of Flow Control**: The language doesn't include conditionals (e.g., `if-else`) or loops (e.g., `while`, `for`).
2. **No Type System**: The language doesn't include a type system, and relies on Python's dynamic types. This could to runtime errors due to type mismatches.
3. **No assignment operations**: The language doesn't include assignment operations for variables, and instead returns the output of each operation right after it is interpreted.
4. **Limited Data Types**: The language only supports integers and booleans constants, without arrays, lists, or decimal numbers.
