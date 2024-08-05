from .lexer import Lexer
from .token import FUNCTION_CONFIGURATION_KEYS, FunctionConfigurationKey, Token,TokenType,BINARY_OPERATIONS
from .errors import ParserError,ErrorCode
from .ast import AST,BinOp,Boolean,FunctionCall,FunctionDecl,Integer,Lambda,NoOp,Param,Program,Statement,Token,TokenType, NotOp, Var

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
        """program: statements"""
        statements = self.statements()

        return Program(statements)

    def statements(self) -> list[Statement]:
        """
        statements: function_declaration statements | expression statements
        """
        statements = []

        while self.current_token is not None and self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.FUNCTION_DECL:
                statements.append(self.function_declaration())    
            else:
                statements.append(self.expression())

        return statements

    def function_declaration(self) -> FunctionDecl:
        """
        <function_declaration> ::= Defun { '<function_config_key>': '<identifier>', '<function_config_key>': <formal_parameters_list>} <expression>
                                 | Defun { '<function_config_key>': <formal_parameters_list>, '<function_config_key>': '<identifier>'} <expression>
        """
        self.eat(TokenType.FUNCTION_DECL)
        self.eat(TokenType.LCURL)

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
                
                function_name = self.current_token.value

                self.eat(TokenType.ID)
                self.eat(TokenType.QUOTE)
            
            else:
                self.eat(TokenType.LPAREN)
                # TODO: breaks here for some reason, debug and check
                arguments = self.formal_parameters_list()
                self.eat(TokenType.RPAREN)
                
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
        
        self.eat(TokenType.RCURL)
        # Match function body <expression>
        expr_node = self.expression()

        return FunctionDecl(
            name=function_name,
            params=arguments,
            expr_node= expr_node
        )

    def formal_parameters_list(self) -> list[Param]:
        """
        <parameter_list> ::= <identifier> | <identifier> "," <parameter_list>
        """

        params = []

        while self.current_token.type == TokenType.ID:
            param = Param(Var(self.current_token))
            params.append(param)
            self.eat(TokenType.ID)
            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
            else:
                break

        return params

    def expression(self) -> AST:
        """
        <expression> ::= <binary_operation>
                       | LPAREN <lambda_expression> RPAREN
                       | <unary_operation>
                       | LPAREN <expression> RPAREN
                       | <identifier>
                       | <integer>
        """

        token = self.current_token

        # Handle integer operations
        if token.type == TokenType.INTEGER_CONST:
            self.eat(TokenType.INTEGER_CONST)
            return Integer(token)

        # Handle boolean const
        elif token.type == TokenType.BOOLEAN_CONST:
            self.eat(TokenType.BOOLEAN_CONST)
            return Boolean(token)
            
        # Handle identifier / reserved keyword
        elif token.type == TokenType.ID:
            return self.unary_operation()
        
        # Handle parenthesized expression
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)

            # Handle Lambda expression
            if self.current_token.type == TokenType.LAMBDA:
                node = self.lambda_expression()
            else:
                node = self.expression()
            self.eat(TokenType.RPAREN)

            return node
        
        # Handle NOT opeartion
        elif token.type == TokenType.NOT:
            node = self.not_operation()
               
        return self.binary_operation()

    def binary_operation(self) -> BinOp:
        left = self.term()

        while self.current_token.type in BINARY_OPERATIONS:
            op_token = self.current_token
            self.eat(op_token.type)
            
            left = BinOp(left=left, op=op_token, right=self.term())

        return left
        
    def term(self) -> AST:
        """
        Term: Parses terms in binary operations
        """

        token = self.current_token

        if token.type == TokenType.INTEGER_CONST:
            self.eat(TokenType.INTEGER_CONST)
            return Integer(token)
        
        elif token.type == TokenType.BOOLEAN_CONST:
            self.eat(TokenType.BOOLEAN_CONST)
            return Boolean(token)
        
        elif token.type == TokenType.ID:
            return self.unary_operation()
        
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node
        
        elif token.type == TokenType.NOT:
            return self.not_operation()
        
        else:
            self.error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=token
            )

    def variable(self):
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(TokenType.ID)
        return node
    
    def unary_operation(self):
        """
        <unary_operation> ::= <function_call> | <not_operation>
        """

        if self.current_token.type == TokenType.ID:
            return self.function_call()
        elif self.current_token.type == TokenType.NOT:
            return self.not_operation()
        
        self.error(
            error_code=ErrorCode.UNEXPECTED_TOKEN,
            token=self.current_token
        )

    def not_operation(self):
        """
        <not_operation> ::= '!' <expression> | '!' <identifier>
        """
        token = self.current_token
        self.eat(TokenType.NOT)

        if self.current_token.type == TokenType.ID:
            return NotOp(token,self.unary_operation())
        else:
            return NotOp(self.expression())

    def lambda_expression(self) -> Lambda:
        """
        <lambda_expression> ::= "Lambd" <identifier> "." <expression>
        """
        self.eat(TokenType.LAMBDA)

        param = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.DOT)

        node = self.expression()

        return Lambda(
            param=param,
            expr_node=node
        )

    def function_call(self) -> FunctionCall:
        """
        <function_call> ::= <identifier> "(" <argument_list> ")"
        """
        func_name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)

        params = self.actual_parameters_list()
        
        return FunctionCall(
            func_name=func_name,
            actual_params=params,
            token=self.current_token
        )
    
    def actual_parameters_list(self) -> list[AST]:
        """
        <argument_list> ::= <expression> | <expression> "," <argument_list>
        """
        actual_params = []

        if self.current_token.type != TokenType.RPAREN:
            actual_params.append(self.expression())

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            actual_params.append(self.expression())

        self.eat(TokenType.RPAREN)

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

        

