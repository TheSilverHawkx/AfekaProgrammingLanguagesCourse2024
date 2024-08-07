from .token import TokenType
from .ast import AST,BinOp,Boolean,FunctionCall,FunctionDecl,Integer,Lambda,NoOp,NotOp,Param,Program,UnaryOp
from .stack import ActivationRecord,CallStack,ARType

class NodeVisitor(object):
    def visit(self, node: AST) -> None:
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self,method_name,self.generic_visit)
        return visitor(node)
    
    def generic_visit(self,node: AST):
        raise Exception(f'No visit_{type(node).__name__} method')
    

class Interpreter(NodeVisitor):
    def __init__(self, tree: AST) -> None:
        self.tree = tree
        self.call_stack = CallStack()

    def visit_Program(self,node: Program):
        ar = ActivationRecord(
            name='PROGRAM',
            type=ARType.PROGRAM,
            nesting_level=1
        )

        self.call_stack.push(ar)

        for statement in node.statements:
            if (output := self.visit(statement)) is not None:
                print(output)

        self.call_stack.pop()
    
    def visit_BinOp(self, node: BinOp):
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
        return node.value
    
    def visit_Boolean(self, node: Boolean) -> bool:
        return node.value
    
    def visit_NotOp(self, node: NotOp):
        return not self.visit(node.expr)
    
    def visit_NoOp(self, node: NoOp):
        pass
    
    def visit_FunctionDecl(self, node: FunctionDecl):
        pass

    def visit_Param(self, node: Param):
        ar = self.call_stack.peek()
        return ar[node.name]

    def visit_UnaryOp(self, node: UnaryOp):
        op_type = node.op.type

        match op_type:
            case TokenType.PLUS:
                return + self.visit(node.expr)
            case TokenType.MINUS:
                return - (self.visit(node.expr))

    def visit_Lambda(self, node: Lambda):
        # TODO: Don't know how this should be implemented yet
        pass

    def visit_FunctionCall(self, node: FunctionCall):
        func_name = node.func_name

        ar = ActivationRecord(
            name=func_name,
            type=ARType.FUNCTION,
            nesting_level=self.call_stack.peek().nesting_level +1
        )

        func_symbol = node.func_symbol

        formal_params = func_symbol.formal_params
        actual_params = node.actual_params

        for param_symbol, arg_node in zip(formal_params,actual_params):
            ar[param_symbol.name] = self.visit(arg_node)

        self.call_stack.push(ar)

        output = self.visit(func_symbol.expr_ast)

        self.call_stack.pop()

        return output

    def interpret(self):
        if (tree:= self.tree) is not None:
            return self.visit(tree)
        
        return ''

        