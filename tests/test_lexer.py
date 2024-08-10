
import pytest
from src.interpreter.lexer import Lexer
from src.interpreter.token import TokenType, Token
from src.interpreter.errors import LexerError

def test_last_token_is_EOF():
    text = ''
    lexer = Lexer(text)

    assert lexer.get_next_token().type == TokenType.EOF

def test_tokenize_keywords_and_identifiers():
    text = "Defun Lambd x y n"
    lexer = Lexer(text)
    tokens: list[Token] = [] 

    while (token := lexer.get_next_token()).type is not TokenType.EOF:
        tokens.append(token)
    
    assert tokens[0].type == TokenType.FUNCTION_DECL
    assert tokens[1].type == TokenType.LAMBDA
    assert tokens[2].type == TokenType.ID and tokens[2].value == 'x'
    assert tokens[3].type == TokenType.ID and tokens[3].value == 'y'
    assert tokens[4].type == TokenType.ID and tokens[4].value == 'n'

def test_tokenize_operators_and_symbols():
    text = "( ) { } + - * / == != > < >= <= && || , : not and or"
    lexer = Lexer(text)
    tokens: list[Token] = [] 

    while (token := lexer.get_next_token()).type is not TokenType.EOF:
        tokens.append(token)
    
    expected_token_types = [
        TokenType.LPAREN, TokenType.RPAREN, TokenType.LCURL, TokenType.RCURL, 
        TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV, 
        TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.GREATER_THAN, TokenType.LESS_THAN, 
        TokenType.GREATER_THAN_EQ, TokenType.LESS_THAN_EQ, TokenType.AND, TokenType.OR,
        TokenType.COMMA, TokenType.COLON, TokenType.NOT,TokenType.AND, TokenType.OR
    ]
    
    for token, expected_type in zip(tokens, expected_token_types):
        assert token.type == expected_type

def test_token_type_identification_case_insensitivity():
    tokens = [
        ('lambd', TokenType.LAMBDA),
        ('LAMBD', TokenType.LAMBDA),
        ('lAmbd', TokenType.LAMBDA),
        ('defun', TokenType.FUNCTION_DECL),
        ('DEFUN', TokenType.FUNCTION_DECL),
        ('deFun', TokenType.FUNCTION_DECL),
        ('x', TokenType.ID),
        ('X', TokenType.ID)
    ]
    for text, expected_token_type in tokens:
        lexer = Lexer(text)

        token = lexer.get_next_token() 
        assert token.type == expected_token_type
        assert token.value == text

def test_tokenize_function_declaration():
    text = "Defun {'name': 'factorial', 'arguments': (n,)}"
    lexer = Lexer(text)
    tokens: list[Token] = [] 

    while (token := lexer.get_next_token()).type is not TokenType.EOF:
        tokens.append(token)
    
    assert tokens[0].type == TokenType.FUNCTION_DECL
    assert tokens[1].type == TokenType.LCURL
    assert tokens[2].type == TokenType.QUOTE
    assert tokens[3].type == TokenType.ID and tokens[3].value == 'name'
    assert tokens[4].type == TokenType.QUOTE
    assert tokens[5].type == TokenType.COLON
    assert tokens[6].type == TokenType.QUOTE
    assert tokens[7].type == TokenType.ID and tokens[7].value == 'factorial'
    assert tokens[8].type == TokenType.QUOTE
    assert tokens[9].type == TokenType.COMMA
    assert tokens[10].type == TokenType.QUOTE
    assert tokens[11].type == TokenType.ID and tokens[11].value == 'arguments'
    assert tokens[12].type == TokenType.QUOTE
    assert tokens[13].type == TokenType.COLON
    assert tokens[14].type == TokenType.LPAREN
    assert tokens[15].type == TokenType.ID and tokens[15].value == 'n'
    assert tokens[16].type == TokenType.COMMA
    assert tokens[17].type == TokenType.RPAREN
    assert tokens[18].type == TokenType.RCURL

def test_unexpected_character():
    text = "@"
    lexer = Lexer(text)
    
    token = None
    with pytest.raises(LexerError):
        lexer.get_next_token()
            
def test_unexpected_float():
    text = "1.20"

    lexer = Lexer(text)

    tokens: list[Token] = []

    while (token := lexer.get_next_token()).type is not TokenType.EOF:
        tokens.append(token)

    expected_token_types = [
        TokenType.INTEGER_CONST,TokenType.DOT, TokenType.INTEGER_CONST
    ]
    
    for token, expected_type in zip(tokens, expected_token_types):
        assert token.type == expected_type

def test_contant_values():
    tokens = [
        ('0', TokenType.INTEGER_CONST,0),
        ('1', TokenType.INTEGER_CONST,1),
        ('2', TokenType.INTEGER_CONST,2),
        ('3', TokenType.INTEGER_CONST,3),
        ('4', TokenType.INTEGER_CONST,4),
        ('5', TokenType.INTEGER_CONST,5),
        ('6', TokenType.INTEGER_CONST,6),
        ('7', TokenType.INTEGER_CONST,7),
        ('8', TokenType.INTEGER_CONST,8),
        ('9', TokenType.INTEGER_CONST,9),
        ('10', TokenType.INTEGER_CONST,10),
        ('100', TokenType.INTEGER_CONST,100),
        ('1.5', TokenType.INTEGER_CONST,1),
        ('True', TokenType.BOOLEAN_CONST,True),
        ('true', TokenType.BOOLEAN_CONST,True),
        ('TRUE', TokenType.BOOLEAN_CONST,True),
        ('False', TokenType.BOOLEAN_CONST,False),
        ('FALSE', TokenType.BOOLEAN_CONST,False),
        ('false', TokenType.BOOLEAN_CONST,False),
    ]

    for text, expected_token_type,expected_value in tokens:
        lexer = Lexer(text)

        token = lexer.get_next_token() 
        assert token.type == expected_token_type
        assert token.value == expected_value
    
def test_ignore_comments():
    text = "# this is a comment x + y"
    lexer = Lexer(text)

    assert lexer.get_next_token().type == TokenType.EOF