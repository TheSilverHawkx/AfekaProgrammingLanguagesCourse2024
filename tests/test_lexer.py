
import pytest
from src.interpreter.lexer import Lexer
from src.interpreter.token import TokenType, Token
from src.interpreter.errors import LexerError

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
        TokenType.GREATER_THAN_EQ, TokenType.GREATER_THAN_EQ, TokenType.AND, TokenType.OR,
        TokenType.COMMA, TokenType.COLON, TokenType.NOT,TokenType.AND, TokenType.OR
    ]
    
    for token, expected_type in zip(tokens, expected_token_types):
        assert token.type == expected_type

def test_tokenize_function_declaration():
    text = "Defun {'name': 'factorial', 'arguments': (n,)}"
    lexer = Lexer(text)
    tokens: list[Token] = [] 

    while (token := lexer.get_next_token()).type is not TokenType.EOF:
        tokens.append(token)
    
    assert tokens[0].type == TokenType.FUNCTION_DECL
    assert tokens[1].type == TokenType.LCURL
    assert tokens[2].type == TokenType.ID and tokens[2].value == 'name'
    assert tokens[3].type == TokenType.COLON
    assert tokens[4].type == TokenType.ID and tokens[4].value == 'factorial'
    assert tokens[5].type == TokenType.COMMA
    assert tokens[6].type == TokenType.ID and tokens[6].value == 'arguments'
    assert tokens[7].type == TokenType.COLON
    assert tokens[8].type == TokenType.LPAREN
    assert tokens[9].type == TokenType.ID and tokens[9].value == 'n'
    assert tokens[10].type == TokenType.COMMA
    assert tokens[11].type == TokenType.RPAREN
    assert tokens[12].type == TokenType.RCURL

def test_unexpected_character():
    text = "Defun @"
    lexer = Lexer(text)
    
    token = None
    with pytest.raises(LexerError):
        while token is not TokenType.EOF:
            token = lexer.get_next_token()

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


    
