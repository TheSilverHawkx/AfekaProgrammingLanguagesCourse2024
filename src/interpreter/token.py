from enum import Enum

class TokenType(Enum):
    # Boolean Operations:
    NOT             = '!'
    AND             = '&&'
    OR              = '||'
    # Comparison Operations
    EQUAL           = '=='
    NOT_EQUAL       = '!='
    GREATER_THAN_EQ = '>='
    LESS_THAN_EQ    = '<='  
    GREATER_THAN    = '>'
    LESS_THAN       = '<'
    # Single-character token types
    PLUS            = '+'
    MINUS           = '-'
    MUL             = '*'
    DIV             = '/'
    MODULO          = '%'
    LPAREN          = '('
    RPAREN          = ')'
    LCURL           = '{'
    RCURL           = '}'
    DOT             = '.'
    COMMENT         = "#"
    QUOTE           = "'"
    COLON           = ':'
    COMMA           = ','
    # Reserved words
    LAMBDA          = 'LAMBD'
    FUNCTION_DECL   = 'DEFUN'
    # MISC
    ID              = 'ID'
    INTEGER_CONST   = 'INTEGER_CONST'
    BOOLEAN_CONST   = 'BOOLEAN_CONST'
    EOF             = 'EOF'

class FunctionConfigurationKey(Enum):
    NAME        = 'name'
    ARGUMENTS   = 'arguments'

def _build_keywords_dictionary(enum: Enum, first_keyword: TokenType, last_keyword: TokenType):
    all_token_types = list(enum)

    start_index = all_token_types.index(first_keyword)
    end_index   = all_token_types.index(last_keyword) +1

    reserved_keywords = {
        token_type.value: token_type
        for token_type in all_token_types[start_index: end_index]
    }

    return reserved_keywords

RESERVED_KEYWORDS = {
    **_build_keywords_dictionary(TokenType, TokenType.LAMBDA,TokenType.FUNCTION_DECL),
    'TRUE': TokenType.BOOLEAN_CONST,
    'FALSE': TokenType.BOOLEAN_CONST
}

LOGICAL_OPERATORS   = _build_keywords_dictionary(TokenType,TokenType.AND,TokenType.OR)
COMPARE_OPERATORS   = _build_keywords_dictionary(TokenType,TokenType.EQUAL, TokenType.LESS_THAN)
ADDITION_OPERATORS  = _build_keywords_dictionary(TokenType,TokenType.PLUS,TokenType.MINUS)
MULT_OPERATORS      = _build_keywords_dictionary(TokenType,TokenType.MUL,TokenType.MODULO)
BINARY_OPERATIONS = [*LOGICAL_OPERATORS,*COMPARE_OPERATORS,*ADDITION_OPERATORS,*MULT_OPERATORS]


FUNCTION_CONFIGURATION_KEYS = _build_keywords_dictionary(FunctionConfigurationKey,FunctionConfigurationKey.NAME,FunctionConfigurationKey.ARGUMENTS)

class Token:
    def __init__(
        self,
        type: TokenType,
        value,
        lineno: int = None,
        column: int = None
    ) -> None:
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column

    def __str__(self):
        return 'Token({type}, {value}, position={lineno}:{column})'.format(
            type=self.type,
            value=repr(self.value),
            lineno=self.lineno,
            column=self.column,
        )
    
    __repr__ = __str__