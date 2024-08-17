from .token import TokenType,Token
from .ast import (
    AST,
    BinOp,
    Boolean,
    FunctionCall,
    FunctionDecl,
    Integer,
    Lambda,
    NoOp,
    NotOp,
    Param,
    Program,
    UnaryOp,
    NestedLambda
)
from .stack import ActivationRecord,CallStack,ARType
from .symbol import CallableSymbol
from .errors import ErrorCode,InterpreterError

class NodeVisitor(object):
    """Base class for traversing nodes in an Abstract Syntax Tree (AST).

    This class provides a mechanism for traversing AST nodes and processing them.
    Subclasses should implement specific `visit_*` methods for handling different node types.

    Usage:
        class CustomVisitor(NodeVisitor):
            def visit_Integer(self, node):
                return node.value

        visitor = CustomVisitor()
        result = visitor.visit(some_ast_node)
    """
    def visit(self, node: AST) -> None:
        """Visits a node in the AST.

        This method determines the appropriate `visit_*` method to call based on 
        the node's type. If no specific method is found, it calls `generic_visit`.

        Args:
            node (AST): The AST node to visit.

        Returns:
            None: Or the result of the specific visit method.
        """
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self,method_name,self.generic_visit)
        return visitor(node)
    
    def generic_visit(self,node: AST):
        raise Exception(f'No visit_{type(node).__name__} method')
    

class Interpreter(NodeVisitor):
    """Interpreter for evaluating an Abstract Syntax Tree (AST).

    The Interpreter class traverses the AST, evaluates expressions, and manages 
    function calls using a call stack.

    Attributes:
        call_stack (CallStack): The stack used to manage activation records during interpretation.

    Usage:
        interpreter = Interpreter()
        result = interpreter.interpret(ast_tree)
    """
    def __init__(self, log_stack = False) -> None:
        self.call_stack = CallStack()
        self.should_log = log_stack

    def log_stack(self,message:str = None):
        if self.should_log:
            if message is not None:
                print(f"@ {message}")
            print(self.call_stack.peek())
            print(self.call_stack)

    def error(self,error_code: ErrorCode, token: Token):
        raise InterpreterError(error_code,token)

    def visit_Program(self,node: Program):
        """Handles a Program node and executes all its statements.

        This method creates a global-level activation record, processes all 
        statements within the program, and then removes the activation record.

        Args:
            node (Program): The Program AST node.
        """
        ar = ActivationRecord(
            name='PROGRAM',
            type=ARType.PROGRAM,
            nesting_level=1
        )

        self.call_stack.push(ar)
        self.log_stack("ENTERING PROGRAM")

        for statement in node.statements:
            output = self.visit(statement)
            if output is not None:
                yield output

        self.call_stack.pop()
    
    def visit_BinOp(self, node: BinOp):
        """Evaluates a binary operation node.

        This method evaluates the left and right operands of the binary operation
        and applies the operation defined by the operator token.

        Args:
            node (BinOp): The binary operation AST node.

        Returns:
            The result of the binary operation.
        """
        op_type = node.op.type

        left_val = self.visit(node.left)

        match op_type:
            case TokenType.AND:
                return left_val and self.visit(node.right)
            case TokenType.OR:
                if left_val:
                    return True
                else:
                    return self.visit(node.right)
            case TokenType.EQUAL:
                return left_val == self.visit(node.right)
            case TokenType.NOT_EQUAL:
                return left_val != self.visit(node.right)
            case TokenType.GREATER_THAN_EQ:
                return left_val >= self.visit(node.right)
            case TokenType.LESS_THAN_EQ:
                return left_val <= self.visit(node.right)
            case TokenType.GREATER_THAN:
                return left_val > self.visit(node.right)
            case TokenType.LESS_THAN:
                return left_val < self.visit(node.right)
            case TokenType.PLUS:
                return left_val + self.visit(node.right)
            case TokenType.MINUS:
                return left_val - self.visit(node.right)
            case TokenType.MUL:
                return left_val * self.visit(node.right)
            case TokenType.DIV:
                return left_val // self.visit(node.right)
            case TokenType.MODULO:
                return left_val % self.visit(node.right)

    def visit_Integer(self, node: Integer) -> int:
        """Handles an Integer node and returns its value.

        Args:
            node (Integer): The Integer AST node.

        Returns:
            int: The integer value of the node.
        """
        return node.value
    
    def visit_Boolean(self, node: Boolean) -> bool:
        """Handles a Boolean node and returns its value.

        Args:
            node (Boolean): The Boolean AST node.

        Returns:
            bool: The boolean value of the node.
        """
        return node.value
    
    def visit_NotOp(self, node: NotOp):
        """Evaluates a logical NOT operation node.

        This method negates the value of the operand node.

        Args:
            node (NotOp): The logical NOT operation AST node.

        Returns:
            bool: The negated value of the operand.
        """
        return not self.visit(node.expr)
    
    def visit_NoOp(self, node: NoOp):
        """Handles NoOp (no operation) nodes.

        This method is called for nodes that do not perform any action. It simply passes.

        Args:
            node (NoOp): The NoOp AST node.
        """
        pass
    
    def visit_FunctionDecl(self, node: FunctionDecl):
        """Handles function declaration nodes.

        The function declation is being handled during the Semantic Analysis phase.
        This method is a placeholder for handling function declarations and does nothing.
        
        Args:
            node (FunctionDecl): The FunctionDecl AST node.
        """
        self.call_stack.peek()[node.func_name] = node.symbol

    def visit_Param(self, node: Param):
        """Retrieves the value of a parameter from the current activation record.

        Since the interpreter is executed after the Semantic Analysis process,
        We can assume the parameter will exist in the current activation record.
        
        Args:
            node (Param): The parameter AST node.

        Returns:
            The value of the parameter.
        """
        return self.call_stack.peek()[node.name]

    def visit_UnaryOp(self, node: UnaryOp):
        """Evaluates a unary operation node.

        This method applies the unary operator (e.g., +, -) to the operand.
        No default case was added to the match operation since Parser should parse
        only a defined set of operators.
        
        Args:
            node (UnaryOp): The unary operation AST node.

        Returns:
            The result of the unary operation.
        """
        op_type = node.op.type

        match op_type:
            case TokenType.PLUS:
                return + self.visit(node.expr)
            case TokenType.MINUS:
                return - (self.visit(node.expr))

    def visit_Lambda(self, node: Lambda):
        return node.symbol

    def visit_NestedLambda(self, node: NestedLambda) :
        current_ar = self.call_stack.peek()
        ar = ActivationRecord(
            name=node.lambda_node.lambda_name,
            type=ARType.FUNCTION,
            nesting_level=self.call_stack.peek().nesting_level +1,
            old_ar=current_ar
        )
        
        
        lambda_symbol = node.lambda_node.symbol

        if lambda_symbol is None:
            self.error(
                error_code=ErrorCode.SYMBOL_NOT_FOUND,
                token=node.lambda_node.token
            )

        formal_params = lambda_symbol.formal_params
        actual_params = node.actual_params

        for param_symbol, arg_node in zip(formal_params,actual_params):
            ar[param_symbol.name] = self.visit(arg_node)

        self.call_stack.push(ar)
        self.log_stack("ADDING FRAME TO STACK")

        current_ar['(return value)'] = self.visit(lambda_symbol.expr_ast)

        self.call_stack.pop()
        self.log_stack("REMOVING FRAME FROM STACK")

        return current_ar['(return value)']

    def visit_FunctionCall(self, node: FunctionCall):
        """Handles function call nodes.

        This method creates a function-level activation record, evaluates 
        the function call by visiting its body, and then removes the activation record.

        Args:
            node (FunctionCall): The FunctionCall AST node.

        Returns:
            The result of the function call.
        """
        current_ar = self.call_stack.peek()
        ar = ActivationRecord(
            name=node.func_name,
            type=ARType.FUNCTION,
            nesting_level=self.call_stack.peek().nesting_level +1,
            old_ar=current_ar
        )
        
        func_symbol: CallableSymbol | None = node.symbol or current_ar[node.func_name]

        if func_symbol is None:
            self.error(
                error_code=ErrorCode.SYMBOL_NOT_FOUND,
                token=node.token
            )
        elif not isinstance(func_symbol, CallableSymbol):
            self.error(
                error_code=ErrorCode.UNEXPECTED_SYMBOL,
                token=node.token
            )

        formal_params = func_symbol.formal_params
        actual_params = node.actual_params

        for param_symbol, arg_node in zip(formal_params,actual_params):
            ar[param_symbol.name] = self.visit(arg_node)

        self.call_stack.push(ar)
        self.log_stack("ADDING FRAME TO STACK")

        current_ar['(return value)'] = self.visit(func_symbol.expr_ast)

        self.call_stack.pop()
        self.log_stack("REMOVING FRAME FROM STACK")

        return current_ar['(return value)']

    def interpret(self,tree: AST):
        """Interprets the given AST.

        This method starts the interpretation process by visiting the root 
        of the AST and returning the final result.

        Args:
            tree (AST): The root of the AST.

        Returns:
            The result of interpreting the AST, or an empty string if the tree is None.
        """
        if tree is not None:
            yield from self.visit(tree)

        
