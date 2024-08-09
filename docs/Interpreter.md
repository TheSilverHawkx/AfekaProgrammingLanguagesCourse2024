
# Interpreter

The interpreter executes the validated AST by traversing it in a pre-order manner. It evaluates expressions, calls functions, and manages the execution context using the call stack.

## Execution Flow

The interpreter starts at the root of the AST and evaluates each node according to its type (e.g., expressions, function calls). The call stack is used to manage the scope and keep track of function calls and returns.

```mermaid
sequenceDiagram
    participant Program as Program
    participant GlobalStack as Global Stack
    participant Function as Function Call
    participant FunctionStack as Function Call Stack

    Program->>GlobalStack: Create Global Stack
    GlobalStack-->>Program: Ready

    Program->>Function: Call Function
    Function->>FunctionStack: Create Function Stack
    FunctionStack-->>Function: Ready

    Function->>FunctionStack: Execute Function Body
    FunctionStack->>FunctionStack: Push new scope (if needed)
    FunctionStack->>FunctionStack: Pop scope (when done)

    FunctionStack-->>Function: Return result
    Function->>GlobalStack: Pop Function Stack

    GlobalStack-->>Program: Continue execution
```