
# Interpreter

The interpreter executes the validated AST by traversing it in a post-order manner. It evaluates expressions, calls functions, and manages the execution context using the call stack.

## Execution Flow

Let's take a look at the following code example:
```
Defun {'name' : 'foo', 'arguments': (x,y)}
  x + y

foo(1,2)

(5 + 3) * (10 - 2) / 4 + (7 % 3) * (2 + 3)
```

The interpreter first identifies the function declaration and stores the function identifier `foo` in its current activation record:
<pre>
Defun {'name' : 'foo', 'arguments': (x,y)}    <<       |                    |                 OUTPUT:
x + y                                                  |                    |
                                                       |--------------------|
foo(1,2)                                               | name: Program      |
                                                       | nesting_level: 1   |
(5 + 3) * (10 - 2) / 4 + (7 % 3) * (2 + 3)             | members: {foo}     |
                                                       +--------------------+
======================================================
OUTPUT:

</pre>

Next, the interpreter evaluates the function call `foo(1,2)`, by creating a new activation record that contains a mapping between the formal parameters `x`, `y` and `1`, `2`:
<pre>
Defun {'name' : 'foo', 'arguments': (x,y)}             |                    |
x + y                                                  |                    |
                                                       |--------------------|
foo(1,2)                                      <<       | name: foo          |
                                                       | nesting_level: 2   |
                                                       | members: {x=1,y=2} |
(5 + 3) * (10 - 2) / 4 + (7 % 3) * (2 + 3)             +--------------------+
                                                       | name: Program      |
                                                       | nesting_level: 1   |
                                                       | members: {foo}     |
                                                       +--------------------+                
======================================================
OUTPUT:

</pre>

After the function's evaluation, the interpreter immediately returns the the output `3` to the user and continue to the next instruction:
<pre>
Defun {'name' : 'foo', 'arguments': (x,y)}             |                    |
x + y                                                  |                    |
                                                       |--------------------|
foo(1,2)                                               | name: Program      |
                                                       | nesting_level: 1   |
(5 + 3) * (10 - 2) / 4 + (7 % 3) * (2 + 3)    <<       | members: {foo}     |
                                                       +--------------------+  
======================================================
OUTPUT:
3
</pre>

After returning the output of the last instruction, the call stack is cleared and the interpreter exists:
<pre>
Defun {'name' : 'foo', 'arguments': (x,y)}             |                    |
x + y                                                  |                    |
                                                       |                    |
foo(1,2)                                               |                    |
                                                       |                    |
(5 + 3) * (10 - 2) / 4 + (7 % 3) * (2 + 3)             |                    |
                                                       +--------------------+  
======================================================
OUTPUT:
3
7
</pre>