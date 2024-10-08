from enum import Enum

class ErrorCode(Enum):
    UNEXPECTED_TOKEN    = 'Unexpected token'
    ID_NOT_FOUND        = 'Identifier not found'
    DUPLICATE_ID        = 'Duplicate id found'
    DUPLICATE_SYMBOL    = 'Duplicate symbol found'
    SYMBOL_NOT_FOUND    = 'Symbol not found'
    UNEQUAL_PARAM_COUNT = 'Function actual parameters count does not match formal parameters count'
    UNEXPECTED_SYMBOL   = 'Unexpected symbol'
    DIV_ZERO            = 'Division by zero'

class Error(Exception):
    def __init__(self, error_code=None, token=None, message=None):
        self.error_code = error_code
        self.token = token
        
        self.message = f'{self.__class__.__name__}: {message if message else str(error_code)}'

class LexerError(Error):
    pass

class ParserError(Error):
    pass

class SemanticError(Error):
    pass

class InterpreterError(Error):
    pass