from enum import Enum

class TokenType(Enum):
    """Enumeration of all token types used by the lexer and parser.

    This Enum defines the various types of tokens that can be identified 
    during the lexical analysis phase.
    """
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
    """Enumeration for function configuration keys.

    This Enum defines the keys used in function configurations.
    """
    NAME        = 'name'
    ARGUMENTS   = 'arguments'

def _build_keywords_dictionary(enum: Enum, first_keyword: TokenType, last_keyword: TokenType):
    """Builds a dictionary of reserved keywords from an Enum range.

    This function constructs a dictionary of reserved keywords by 
    extracting a slice of Enum members between the specified start 
    and end members.

    Args:
        enum (Enum): The Enum class containing the keywords.
        first_keyword (TokenType): The first keyword in the range.
        last_keyword (TokenType): The last keyword in the range (inclusive).

    Returns:
        dict: A dictionary mapping keyword strings to their corresponding Enum members.
    """
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
BINARY_OPERATIONS   = [*LOGICAL_OPERATORS,*COMPARE_OPERATORS,*ADDITION_OPERATORS,*MULT_OPERATORS]

FUNCTION_CONFIGURATION_KEYS = _build_keywords_dictionary(FunctionConfigurationKey,FunctionConfigurationKey.NAME,FunctionConfigurationKey.ARGUMENTS)

class Token:
    """Represents a token produced by the lexer.

    A token is a tuple of a token type, a value, and optionally the line 
    and column where the token appears in the source code.

    Attributes:
        type (TokenType): The type of the token (e.g., ID, INTEGER_CONST).
        value (Any): The value of the token (e.g., 'x', 42).
        lineno (int, optional): The line number where the token appears.
        column (int, optional): The column number where the token appears.

    Usage:
        token = Token(TokenType.ID, 'x', lineno=1, column=5)
        print(token)
    """
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
