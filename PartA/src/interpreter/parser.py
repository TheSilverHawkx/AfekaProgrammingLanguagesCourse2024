from .lexer import Lexer
from .token import (
    COMPARE_OPERATORS,
    FUNCTION_CONFIGURATION_KEYS,
    LOGICAL_OPERATORS,
    FunctionConfigurationKey,
    Token,
    TokenType,
    ADDITION_OPERATORS,MULT_OPERATORS
)
from .errors import ParserError,ErrorCode
from .ast import (
    AST,
    BinOp,
    Boolean,
    FunctionCall,
    FunctionDecl,
    Integer,
    Lambda,
    NoOp,
    Param,
    Program,
    NotOp,
    UnaryOp,
    NestedLambda
)

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current_token = self.get_next_token()

    def get_next_token(self) -> Token:
        return self.lexer.get_next_token()
    
    def error(self,error_code: ErrorCode, token: Token) -> None:
        raise ParserError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )
    
    def eat(self, token_type: TokenType):
        """
        Validate the `TokenType` of `current_token`.
        If `current_token` type matches `token_type`: get the next token from the lexer,
        otherwise: throw an error        
        """
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token
            )

    def program(self) -> Program:
        """
        <program> ::= <statement_list>
        """
        statements = self.statement_list()

        return Program(statements)
    
    def statement_list(self) -> list[AST]:
        """
        <statement_list> ::= <statement> | <statement> <statement_list>
        """
        results = []

        while self.current_token is not None and self.current_token.type != TokenType.EOF:
            results.append(self.statement())

        return results 

    def empty(self) -> NoOp:
        """An empty node"""
        return NoOp()
    
    def statement(self) -> AST:
        """
        <statement> ::= <empty>
                      | <lambda_decleration>
                      | <function_declaration>
                      | <expression> 
                      | "(" <statement> ")"
        """
        if self.current_token.type == TokenType.LPAREN and self.lexer.peek_next_token().type == TokenType.LAMBDA:
            return self.lambda_declaration()
        
        elif self.current_token.type == TokenType.FUNCTION_DECL:
            return self.function_declaration()
        
        elif self.current_token.type in (
            TokenType.ID,
            TokenType.BOOLEAN_CONST,
            TokenType.INTEGER_CONST,
            TokenType.LPAREN,
            TokenType.PLUS,
            TokenType.NOT,
            TokenType.MINUS
            ):
            return self.logical_expr()
        elif self.current_token.value == '':
            return self.empty()        
        else:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token
            )

    def function_declaration(self) -> FunctionDecl:
        """
        <function_declaration> ::= "Defun" "{" <function_conf_name> "," <function_conf_args> "}"
                         | "Defun" "{" <function_conf_args> "," <function_conf_name> "}"

        <function_conf_name> ::= "'" "name" "'" ":" "'" ID "'"
        <function_conf_args> ::= "'" "arguments" "'" ":" "(" <formal_parameters> ")"
        """
        function_token = self.current_token

        self.eat(TokenType.FUNCTION_DECL)
        self.eat(TokenType.LCURL)

        function_config = { x.value: None for x in FunctionConfigurationKey }

        while self.current_token is not None and self.current_token.type is not TokenType.RCURL:
            self.eat(TokenType.QUOTE)

            if self.current_token.value not in FUNCTION_CONFIGURATION_KEYS:
                self.error(
                    error_code=ErrorCode.UNEXPECTED_TOKEN,
                    token=self.current_token
                )

            key = self.current_token.value
            self.eat(TokenType.ID)
            self.eat(TokenType.QUOTE)
            self.eat(TokenType.COLON)

            if key == FunctionConfigurationKey.NAME.value:
                self.eat(TokenType.QUOTE)

                if self.current_token.type is not TokenType.ID:
                    self.error(
                        error_code=ErrorCode.UNEXPECTED_TOKEN,
                        token=self.current_token
                    )
                
                function_config[FunctionConfigurationKey.NAME.value] = self.current_token.value

                self.eat(TokenType.ID)
                self.eat(TokenType.QUOTE)
            
            else:
                self.eat(TokenType.LPAREN)
                function_config[FunctionConfigurationKey.ARGUMENTS.value] = self.formal_parameters_list()
                self.eat(TokenType.RPAREN)
                
            if self.current_token.type != TokenType.RCURL:
                self.eat(TokenType.COMMA)
        

        self.eat(TokenType.RCURL)
        # Match function body <expression>
        expr_node = self.logical_expr()

        for key in FunctionConfigurationKey:
            if function_config[key.value] is None:
                self.error(
                    error_code=ErrorCode.ID_NOT_FOUND,
                    token = function_token
                )

        return FunctionDecl(
            name=function_config[FunctionConfigurationKey.NAME.value],
            params=function_config[FunctionConfigurationKey.ARGUMENTS.value],
            expr_node= expr_node
        )

    def formal_parameters_list(self) -> list[Param]:
        """
        <formal_parameters> ::= <identifier> | <identifier> ',' | <identifier> ',' <formal_parameters>
        """
        params = []

        while self.current_token.type == TokenType.ID:
            params.append(Param(self.current_token))
            self.eat(TokenType.ID)

            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
            else:
                break

        return params

    def logical_expr(self) -> AST:
        """
        <logical_expr> ::= <compare_expr> | <compare_expr> <binary_op> <logical_expr>
        """        
        left = self.compare_expr()

        while self.current_token is not None and self.current_token.value in LOGICAL_OPERATORS:
            op_token = self.current_token
            self.eat(op_token.type)

            left = BinOp(left=left,op=op_token,right=self.compare_expr())
        
        return left
    
    def compare_expr(self) -> AST:
        """
        <compare_expr> ::= <addition_expr> | <addition_expr> <compare_op> <addition_expr>
        """

        left = self.addition_expr()

        op_token = self.current_token
        
        if op_token.value in COMPARE_OPERATORS:
            self.eat(op_token.type)
        else:
            return left
            
        return BinOp(left=left,op=op_token,right=self.addition_expr())
        
    def addition_expr(self) -> AST:
        """
        <addition_expr> ::= <multiplication_expr> | <multiplication_expr> <addition_op> <addition_expr>
        """

        left = self.multiplication_expr()

        while self.current_token is not None and self.current_token.value in ADDITION_OPERATORS:
            op_token = self.current_token
            self.eat(op_token.type)

            left = BinOp(left=left,op=op_token,right=self.addition_expr())
        
        return left
        
    def multiplication_expr(self) -> AST:
        """
        <multiplication_expr> ::= <factor> | <factor> <mult_op> <multiplication_expr>
        """

        if self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            self.eat(token.type)
            return UnaryOp(token,self.factor())
        
        left = self.factor()

        while self.current_token is not None and self.current_token.value in MULT_OPERATORS:
            op_token = self.current_token
            self.eat(op_token.type)

            left = BinOp(left=left, op=op_token,right=self.multiplication_expr())

        return left
    
    def factor(self):
        """
        <factor> ::= <integer>
                   | <boolean>
                   | <function_call>
                   | <identifier>
                   | "(" <logical_expr> ")"
                   | "!" <factor>
                   | "not" <factor>
                   | <nested_lambda>
        """
        token = self.current_token

        if token.type == TokenType.NOT:
            self.eat(TokenType.NOT)
            return NotOp(self.factor())

        if token.type == TokenType.BOOLEAN_CONST:
            self.eat(TokenType.BOOLEAN_CONST)
            return Boolean(token)
        
        elif self.current_token.type == TokenType.LPAREN:
            if self.lexer.peek_next_token().type == TokenType.LAMBDA:
                return self.nested_lambda()
            else:
                self.eat(TokenType.LPAREN)
                node = self.logical_expr()
                self.eat(TokenType.RPAREN)
                return node
        
        elif token.type == TokenType.INTEGER_CONST:
            self.eat(TokenType.INTEGER_CONST)
            return Integer(token)
        
        elif token.type == TokenType.ID and self.lexer.peek_next_token().type == TokenType.LPAREN:
            return self.function_call()
        elif token.type == TokenType.ID:
            self.eat(TokenType.ID)
            return Param(token)
        
        else:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=token
            )
        
    def lambda_declaration(self) -> Lambda:
        """
        <lambda_decleration> ::= "(" "Lambd" <formal_parameters> "." <logical_expr> ")"
                               | "(" "Lambd" <formal_parameters> "." <lambda_declaration> ")"
        """
        token = self.current_token
        self.eat(TokenType.LPAREN)
        self.eat(TokenType.LAMBDA)

        params = self.formal_parameters_list()

        self.eat(TokenType.DOT)
        
        if (
            self.lexer.peek_next_token().type == TokenType.LPAREN and
            self.lexer.peek_next_token(2).type == TokenType.LAMBDA
        ):
            node = self.lambda_declaration()
        else:
            node = self.logical_expr()
        
        self.eat(TokenType.RPAREN)

        return Lambda(
            token=token,
            formal_parameters=params,
            expr_node=node
        )

    def nested_lambda(self) -> NestedLambda:
        """
        <nested_lambda> ::= <lambda_decleration> "(" <actual_parameters> ")"
        """
        lambda_node = self.lambda_declaration()

        self.eat(TokenType.LPAREN)
        
        actual_param_nodes = self.actual_parameters()
        
        self.eat(TokenType.RPAREN)
        
        return NestedLambda(
            lambda_node=lambda_node,
            actual_params=actual_param_nodes
        )

    def function_call(self) -> FunctionCall:
        """
        <function_call> ::= ID "(" <actual_parameters> ")"
        """
        token = self.current_token
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)

        params = self.actual_parameters()
        self.eat(TokenType.RPAREN)
        
        return FunctionCall(
            actual_params=params,
            token=token
        )
    
    def actual_parameters(self) -> list[AST]:
        """
        <actual_parameters> ::= <logical_expr>
                              | <logical_expr> ","
                              | <logical_expr> "," <actual_parameters>
                              | <empty>
                              | <lambda_decleration> ","  <actual_parameters>
                              | <lambda_decleration> ","
                              | <lambda_decleration>
        """  
        actual_params = []

        while self.current_token is not None and self.current_token.type != TokenType.RPAREN:
            if (
                self.current_token.type == TokenType.LPAREN and
                self.lexer.peek_next_token().type == TokenType.LAMBDA
            ):
                actual_params.append(self.lambda_declaration())
            else:
                actual_params.append(self.logical_expr())

            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)

        return actual_params
    
    def parse(self) -> Program:
        """
        Parse input code into AST tree for execution
        """

        node = self.program()

        if self.current_token.type != TokenType.EOF:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token
            )

        return node

        

