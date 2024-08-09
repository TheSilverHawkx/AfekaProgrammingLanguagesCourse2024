
# Call Stack

The call stack is used by the interpreter to keep track of active subroutines or function calls. Each time a function is called, a new frame is pushed onto the stack. When the function returns, the frame is popped off, and control is returned to the calling function.

This mechanism ensures that the interpreter correctly handles nested function calls and scope management.