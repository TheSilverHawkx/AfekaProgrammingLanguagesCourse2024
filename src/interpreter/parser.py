from .lexer import Lexer
from .token import Token,TokenType,BINARY_OPERATIONS
from .errors import ParserError,ErrorCode
from .ast import AST,BinOp,Boolean,FunctionCall,FunctionDecl,Integer,Lambda,NoOp,Param,Program,Statement,Token,TokenType, NotOp

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current_token = self._get_next_token()

    def _get_next_token(self) -> Token:
        return self.lexer.get_next_token()
    
    def _error(self,error_code: ErrorCode, token: Token) -> None:
        raise ParserError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )
    
    def _eat(self, token_type: TokenType):
        """
        Validate the `TokenType` of `current_token`.
        If `current_token` type matches `token_type`: get the next token from the lexer,
        otherwise: throw an error        
        """
        if self.current_token.type == token_type:
            self.current_token = self._get_next_token()
        else:
            self._error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token
            )

    def _program(self) -> Program:
        """program: statements"""
        statements = self._statements()

        return Program(statements)

    def _statements(self) -> list[Statement]:
        """
        statements: function_declaration statements | expression statements
        """
        statements = []

        while self.current_token is not None:
            if self.current_token.type == TokenType.FUNCTION_DECL:
                statements.append(self._function_declaration())    
            else:
                statements.append(self._expression())

        return statements

    def _function_declaration(self) -> FunctionDecl:
        """
        <function_declaration> ::= "Defun" "{" "'name':'"<identifier>"'," "'arguments':" "(" <formal_parameters_list> ")" "}" <expression>
        """
        self._eat(TokenType.FUNCTION_DECL)
        self._eat(TokenType.LCURL)
        
        function_details = {}

        # Match 'name':'<identifier>',
        self._eat(TokenType.QUOTE)

        if self.current_token.value != "name":
            self._error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token
            )

        self._eat(TokenType.ID)
        self._eat(TokenType.QUOTE)
        self._eat(TokenType.COLON)

        self._eat(TokenType.QUOTE)
        function_details["name"] = self.current_token.value        
        self._eat(TokenType.ID)
        self._eat(TokenType.QUOTE)
        self._eat(TokenType.COMMA)

        # Match 'arguments':(<parameter_list>)}
        self._eat(TokenType.QUOTE)
        if self.current_token.value != "arguments":
            self._error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token
            )

        self._eat(TokenType.QUOTE)
        self._eat(TokenType.COLON)
        self._eat(TokenType.LPAREN)
        function_details["params"] = self._formal_parameters_list()
        self._eat(TokenType.RPAREN)
        self._eat(TokenType.RCURL)
        
        # Match function body <expression>
        function_details['expr_node'] = self._expression()

        return FunctionDecl(**function_details)

    def _expression(self):
        """
        expression: binary_operation | lambda_expression | unary_operation | (expression) | identifier | integer
        """
        # Handle binary operations
        if self.current_token.type == TokenType.INTEGER_CONST:
            node = self._binary_operation()
            
        
        # Handle NOT opeartion
        elif self.current_token.type == TokenType.NOT:
            node = self._not_operation()
        
        
            node = self._lambda()

        # Handle parenthesized expression
        elif self.current_token.type == TokenType.LPAREN:
            self._eat(TokenType.LPAREN)

            # Handle Lambda expression
            if self.current_token.type == TokenType.LAMBDA:
                node = self._lambda()
            else:
                node = self._expression()
            self._eat(TokenType.RPAREN)
        
        else:
            node = self._function_call()
        
        return node

    def _formal_parameters_list(self) -> list[Param]:
        pass

    def _actual_parameters_list(self) -> list[AST]:
        """actual_parameters_list : expression | expression,actual_parameters_list"""
        actual_params = []

        if self.current_token.type != TokenType.RPAREN:
            actual_params.append(self._expression())

        while self.current_token.type == TokenType.COMMA:
            self._eat(TokenType.COMMA)
            actual_params.append(self._expression())

        self._eat(TokenType.RPAREN)

        return actual_params
            

    def _not_operation(self):
        """not_operation: !expression | !identifier"""
        self._eat(TokenType.NOT)

        if self.current_token.type == TokenType.ID:
            return NotOp(self.current_token)
        else:
            return NotOp(self._expression())       

    def _binary_operation(self) -> BinOp:
        left_value = self.current_token
        self._eat(TokenType.ID)

    def _lambda(self) -> Lambda:
        """lambda_expression : Lambd identifier. expression"""
        self._eat(TokenType.LAMBDA)

        param = self.current_token.value
        self._eat(TokenType.ID)
        self._eat(TokenType.DOT)

        node = self._expression()

        return Lambda(
            param=param,
            expr_node=node
        )

    def _function_call(self) -> FunctionCall:
        """function_call: identifier(actual_parameters_list)"""
        func_name = self.current_token.value
        self._eat(TokenType.ID)
        self._eat(TokenType.LPAREN)

        params = self._actual_parameters_list()
        
        return FunctionCall(
            func_name=func_name,
            actual_params=params,
            token=self.current_token
        )



    def parse(self) -> Program:
        """
        Parse input code into AST tree for execution
        """

        node = self._program()

        if self.current_token.type != TokenType.EOF:
            self._error(
                error_code=ErrorCode.UNEXPECTED_TOKEN,
                token=self.current_token
            )

        return node

        

