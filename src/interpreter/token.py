from enum import Enum

class TokenType(Enum):
    # Boolean Operations:
    AND             = '&&'
    OR              = '||'
    NOT             = '!'
    # Comparison Operations
    EQUAL           = '=='
    NOT_EQUAl       = '!='
    GREATER_THAN    = '>'
    LESS_THAN       = '<'
    GREATER_THAN_EQ = '>='
    LESS_THAN_EQ    = '<='  
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
    LAMBDA          = 'Lambd'
    FUNCTION_DECL   = 'Defun'
    # MISC
    ID              = 'ID'
    INTEGER_CONST   = 'INTEGER_CONST'
    BOOLEAN_CONST   = 'BOOLEAN_CONST'
    EOF             = 'EOF'


def _build_keywords_dictionary(first_keyword: TokenType, last_keyword: TokenType):
    all_token_types = list(TokenType)

    start_index = all_token_types.index(first_keyword)
    end_index   = all_token_types.index(last_keyword) +1

    reserved_keywords = {
        token_type.value: token_type
        for token_type in all_token_types[start_index: end_index]
    }

    return reserved_keywords

RESERVED_KEYWORDS = {
    **_build_keywords_dictionary(TokenType.LAMBDA,TokenType.FUNCTION_DECL),
    'True': TokenType.BOOLEAN_CONST,
    'False': TokenType.BOOLEAN_CONST
}

BINARY_OPERATIONS = _build_keywords_dictionary(TokenType.AND,TokenType.MODULO)

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