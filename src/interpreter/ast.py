from .token import TokenType,Token
from uuid import uuid4

class AST:
    pass


class Statement(AST):
    def __init__(self,name) -> None:
        self.name = name

class Program(AST):
    def __init__(self, statements: list[Statement]) -> None:
        self.statements = statements


class Integer(AST):
    """ Constant Integer AST Node"""
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

class Boolean(AST):
    """ Constant Boolean AST Node"""
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value

class BinOp(AST):
    """ Binary Operation AST Node"""
    def __init__(self, left: Token, op: Token, right: Token):
        self.left = left
        self.token = self.op = op
        self.right = right

class UnaryOp(AST):
    """ Unary Operation AST Node"""
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class NotOp(AST):
    """ Not Operation AST Node"""
    def __init__(self,expr: AST) -> None:
        self.expr = expr

class Param(AST):
    """ Function Parameter AST Node"""
    def __init__(self, token: Token) -> None:
        self.token = token
        self.name = token.value

class FunctionDecl(AST):
    """ Function Declaration AST Node"""
    def __init__(self, name:str, params: list[Param], expr_node):
        self.func_name = name
        self.params = params
        self.expr_node = expr_node
    
class FunctionCall(AST):
    def __init__(self, token: Token, actual_params ) -> None:
        self.token = token
        self.func_name = token.value
        self.actual_params = actual_params
        self.func_symbol = None

class Lambda(AST):
    """ Lambda Decleration AST Node"""
    def __init__(self,param:Param, expr_node: AST) -> None:
        self.lambda_name:str = f"lambda_{uuid4()}"
        self.param = param
        self.expr_node = expr_node

class NoOp(AST):
    """ Empty Operation AST Node"""
    pass





