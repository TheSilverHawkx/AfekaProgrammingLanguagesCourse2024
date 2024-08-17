
# Call Stack

The call stack is used by the interpreter to keep track of function calls and lambda executions. Each time a function is called, a new frame is pushed onto the stack. When the function returns, the frame is popped off, and control is returned to the calling function.

This mechanism ensures that the interpreter correctly handles nested function calls and scope management.

## Example
Let's look at the following code example:
```
Defun {'name' : 'foo', 'arguments': (x,y)}
  x + y

foo(1,2)
```
The program defined a function named `foo` and it has two parameters: `x` and `y`.
At phase 1, right after we start the execution of this code, we initialize our call stack and create our PROGRAM activation record.

Then at phase 2, the function `foo` is declared function is saved into our current activation record.

<div style="text-align: center;">
  <pre>
                |                      |     |                      |
                |                      |     |                      |
                |                      |     |                      |
                |                      |     |                      |
                |                      |     |                      |
                |                      |     |                      |
                +----------------------+     +----------------------+
                | name: Main Program   |     | name: Main Program   |
                | level: 1             |     | level: 1             |
                | context:             |     | context:             |
                | {}                   |     | { 'foo': <function>} | 
                +----------------------+     +----------------------+
                          (1)                           (2)
  </pre>
</div>

Next, when we a function is called, we create a new activation record for the function's scope:
<div style="text-align: center;">
  <pre>
                |                      |
                |                      |
                +----------------------+
                | name: foo            |
                | level: 2             |
                | context:             |
                | {'x':1, 'y':2 }      |
                +----------------------+
                | name: Main Program   |
                | level: 1             |
                | context:             |
                | { 'foo':  function } |
                +----------------------+

  </pre>
</div>
