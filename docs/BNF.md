# BNF Grammar for Custom Language

## Grammar Structure

This document provides a detailed description of the Backus-Naur Form (BNF) grammar of the programming language.

### Production Rules

```bnf
<program> ::= <statement_list>
<statement_list> ::= <statement> | <statement> <statement_list>

<statement> ::= <empty>
              | <lambda_decleration>
              | <function_declaration>
              | <logical_expr> 
              | "(" <statement> ")"

<lambda_decleration> ::= "(" "Lambd" <identifier> "." <logical_expr> ")"

<function_declaration> ::= "Defun" "{" <function_conf_name> "," <function_conf_args> "}" <logical_expr>
                         | "Defun" "{" <function_conf_args> "," <function_conf_name> "}" <logical_expr>

<function_conf_name> ::= "'" "name" "'" ":" "'" ID "'"
<function_conf_args> ::= "'" "arguments" "'" ":" "(" <formal_parameter_list> ")"

<formal_parameter_list> ::= <identifier> | <identifier> ',' | <identifier> ',' <formal_parameter_list>


<logical_expr>  ::= <compare_expr> | <compare_expr> <binary_op> <logical_expr>
<compare_expr>  ::= <additive_expr> | <additive_expr> <compare_op> <additive_expr>
<additive_expr> ::= <multiplicative_expr> | <multiplicative_expr> <addition_op> <additive_expr>
<multiplicative_expr> ::= <factor>
                        | <factor> <mult_op> <multiplicative_expr>
                        | <addition_op> <factor>

<factor> ::= <integer>
           | <boolean>
           | <function_call>
           | <identifier>
           | "(" <logical_expr> ")"
           | "!" <logical_expr>
           | "not" <logical_expr>

<function_call> ::= <identifier> "(" <function_call_parameters> ")"
<function_call_parameters> ::= <logical_expr>
                             | <logical_expr> ","
                             | <logical_expr> "," <function_call_parameters>
                             | <empty>

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
### Symbol Structure
- **`<program>`**: Represents the entire program.
  ```bnf
  <program> ::= <statement_list>
  ```

### Statement List
- **`<statement_list>`**: A sequence of statements.
  ```bnf
  <statement_list> ::= <statement> | <statement> <statement_list>
  ```

### Statements
- **`<statement>`**: Represents different types of executable instructions within the program.
  ```bnf
  <statement> ::= <empty>
                | <lambda_decleration>
                | <function_declaration>
                | <logical_expr> 
                | "(" <statement> ")"
  ```

### Lambda Declaration
- **`<lambda_decleration>`**: Defines an anonymous function (lambda) with one parameter and a body expression.
  ```bnf
  <lambda_decleration> ::= "(" "Lambd" <identifier> "." <logical_expr> ")"
  ```

### Function Declaration
- **`<function_declaration>`**: Defines a named function with arguments and a body expression.
  ```bnf
  <function_declaration> ::= "Defun" "{" <function_conf_name> "," <function_conf_args> "}" <logical_expr>
                           | "Defun" "{" <function_conf_args> "," <function_conf_name> "}" <logical_expr>
  ```

### Function Configuration
- **`<function_conf_name>`**: Specifies the name of the function.
  ```bnf
  <function_conf_name> ::= "'" "name" "'" ":" "'" ID "'"
  ```

- **`<function_conf_args>`**: Specifies the arguments of the function.
  ```bnf
  <function_conf_args> ::= "'" "arguments" "'" ":" "(" <formal_parameter_list> ")"
  ```

### Formal Parameter List
- **`<formal_parameter_list>`**: Defines the list of parameters for a function.
  ```bnf
  <formal_parameter_list> ::= <identifier> | <identifier> ',' | <identifier> ',' <formal_parameter_list>
  ```

### Logical Expressions
- **`<logical_expr>`**: Represents logical or comparison expressions.
  ```bnf
  <logical_expr>  ::= <compare_expr> | <compare_expr> <binary_op> <logical_expr>
  ```

### Comparison Expressions
- **`<compare_expr>`**: Defines expressions involving comparisons.
  ```bnf
  <compare_expr>  ::= <additive_expr> | <additive_expr> <compare_op> <additive_expr>
  ```

### Additive Expressions
- **`<additive_expr>`**: Defines expressions involving addition or subtraction.
  ```bnf
  <additive_expr> ::= <multiplicative_expr> | <multiplicative_expr> <addition_op> <additive_expr>
  ```

### Multiplicative Expressions
- **`<multiplicative_expr>`**: Defines expressions involving multiplication, division, or modulus.
  ```bnf
  <multiplicative_expr> ::= <factor>
                          | <factor> <mult_op> <multiplicative_expr>
                          | <addition_op> <factor>
  ```

### Factors
- **`<factor>`**: The simplest elements in expressions, including integers, booleans, function calls, and identifiers.
  ```bnf
  <factor> ::= <integer>
             | <boolean>
             | <function_call>
             | <identifier>
             | "(" <logical_expr> ")"
             | "!" <logical_expr>
             | "not" <logical_expr>
  ```

### Function Call
- **`<function_call>`**: Represents a call to a function with parameters.
  ```bnf
  <function_call> ::= <identifier> "(" <function_call_parameters> ")"
  ```

- **`<function_call_parameters>`**: The parameters passed to a function call.
  ```bnf
  <function_call_parameters> ::= <logical_expr>
                               | <logical_expr> ","
                               | <logical_expr> "," <function_call_parameters>
                               | <empty>
  ```

### Terminal Symbols

- **`<integer>`**: A numeric value.
  ```bnf
  <integer> ::= <digit> | <digit> <integer>
  ```

- **`<identifier>`**: A name or label, made up of characters and digits.
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

## Explanation of Symbols

- **Non-Terminal Symbols**: These are symbols that can be expanded into other symbols or terminal symbols. For example, `<statement>`, `<logical_expr>`, `<identifier>`.
  
- **Terminal Symbols**: These are the basic elements from which programs are constructed, such as `"True"`, `"Defun"`, `","`, `"("`, and `"0"`.
  
- **Operators**: These include arithmetic, logical, and comparison operators like `+`, `-`, `*`, `/`, `&&`, `||`, `==`, `!=`, etc.
  
- **Literals**: Specific values like booleans (`True`, `False`) and integers (e.g., `123`).

- **Functions**: Represented by the `<function_declaration>`, `<lambda_decleration>`, and `<function_call>` rules, which define how functions are declared and invoked.

## Pros and Cons of the BNF Structure

### Pros:
1. **Modularity**: The BNF grammar is well-structured, separating different components like expressions, functions, and statements, making it easier to extend or modify.
2. **Expressiveness**: Supports a variety of logical and arithmetic operations, function declarations, and lambda expressions, making it versatile.
3. **Readability**: The clear distinction between different components (e.g., statements, expressions) improves readability and maintainability.
4. **Reusability**: Non-terminal symbols like `<logical_expr>` and `<statement_list>` are reused in multiple places, promoting DRY (Don't Repeat Yourself) principles.

### Cons:
1. **Complexity**: The grammar may be complex for simple use cases, with multiple layers of abstraction for expressions and functions.
2. **Limited Functionality**: Lacks features like loops, conditionals, or more advanced data structures, limiting its use for more complex programming tasks.
3. **Ambiguity in Function Configuration**: The `<function_declaration>` rule allows for different orders of name and arguments, which could lead to parsing complexity or errors.
4. **No Error Handling**: The grammar doesn't account for error handling or exceptions, which are crucial for robust programming languages.

### Limitations of the Language

1. **Lack of Control Structures**: The language doesn't include conditionals (e.g., `if-else`) or loops (e.g., `while`, `for`), limiting its capability to handle complex logic.
2. **No Type System**: The BNF doesn't define a type system, which could lead to runtime errors due to type mismatches.
3. **Minimal Data Structures**: The grammar only supports basic types like integers and booleans, without arrays, lists, or more complex data structures.
4. **Scalability**: The language may not scale well for larger programs due to the lack of modular constructs like classes or modules.
5. **Ambiguity in Operator Precedence**: The BNF does not explicitly define the precedence and associativity of operators, which could lead to ambiguity in complex expressions. 

This BNF provides a basic framework for a simple functional programming language with support for functions, logical expressions, and basic operations. However, it would require significant expansion and refinement for use in more complex or large-scale programming tasks.