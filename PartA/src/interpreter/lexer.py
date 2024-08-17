from .token import Token,TokenType,RESERVED_KEYWORDS
from .errors import LexerError

IS_ALPHABETIC = lambda char: char.isalpha()
IS_ALPHANUMERIC = lambda char: char.isalnum()
IS_NUMERIC = lambda char: char.isdigit()

class Lexer:
    """Lexical analyzer (lexer) for converting input text into tokens.

    The Lexer class reads input text and breaks it down into tokens that 
    can be used by a parser for further analysis. It handles various token 
    types such as identifiers, reserved keywords, operators, and literals.

    Attributes:
        text (str): The input text to be tokenized.
        pos (int): The current index position in the input text.
        current_char (str or None): The current character being analyzed.
        lineno (int): The current line number in the input text.
        column (int): The current column number in the input text.

    Usage:
        lexer = Lexer("1 + 1")
        token = lexer.get_next_token()
    """
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if len(self.text) > 0 else None
        self.lineno = 1
        self.column = 1
    
    def _error(self) -> None:
        """Raises a LexerError with the current character's position.

        This method is called when the lexer encounters an invalid character 
        or sequence in the input text.
        """
        raise LexerError(
            "Lexer error on '{lexeme}' line: {lineno} column: {column}".format(
                lexeme = self.current_char,
                lineno= self.lineno,
                column = self.column
            )
        )
    
    def advance(self) -> None:
        """Advances the `pos` pointer and updates the `current_char` variable.

        This method moves the lexer to the next character in the input text, 
        updating the position, line number, and column number accordingly.
        """

        if self.current_char == '\n':
            self.lineno +=1
            self.column = 0

        self.pos += 1

        # Check if EOF was reached, else extract the next char
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            self.column += 1

    def peek(self) -> str:
        """Returns the character at `self.pos + 1` without consuming it.

        This method allows the lexer to look ahead one character in the input text.

        Returns:
            str: The next character in the input text, or None if at the end.
        """
        peek_pos = self.pos + 1

        return self.text[peek_pos] if peek_pos <= len(self.text) - 1 else None
    
    def peek_next_token(self, n = 1) -> Token:
        """Peeks at n-th token from the current position without consuming it.

        This method saves the current position, advances to get the n-th token, 
        then restores the original position.

        Returns:
            Token: The n-th token in the input text from the current position.
        """
        origin_pos = self.pos
        origin_lineo = self.lineno
        origin_column = self.column

        for i in range(0,n):
            token = self.get_next_token()
            
        self.pos = origin_pos
        self.lineno = origin_lineo
        self.column = origin_column
        self.current_char = self.text[origin_pos]

        return token
    
    def skip_whitespace(self) -> None:
        """Advances the `pos` pointer until the next non-whitespace character.

        This method is used to ignore spaces, tabs, and other whitespace characters
        in the input text.
        """
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self) -> None:
        """Advances the `pos` pointer until the end of the comment line (i.e., new line).

        This method is used to skip over one-line comments in the input text, which are 
        typically ignored by the lexer.
        """
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        self.advance()
    
    def __get_multichar_by_condition(self, condition) -> str:
        """Returns a multi-character sequence from `text` based on a `condition` function.

        This method is used to extract identifiers, multi-digit numbers, reserved 
        keywords, etc., from the input text.

        Args:
            condition (function): A function that defines the condition for extracting characters.

        Returns:
            str: A sequence of characters that match the specified condition.

        Usage:
            value = self.__get_multichar_by_condition(lambda char: char.isalpha())
        """
        result = ''
        while self.current_char is not None and condition(self.current_char):
            result += self.current_char
            self.advance()
        
        return result

    def integer(self) -> Token:
        """Returns a multi-digit positive integer token from `text`.

        This method converts a sequence of numeric characters into an 
        integer token.

        Returns:
            Token: A token representing the integer literal.
        """
        token = Token(type=TokenType.INTEGER_CONST, value=None, lineno=self.lineno, column=self.column)

        result = self.__get_multichar_by_condition(IS_NUMERIC)

        token.value = int(result)

        return token
        
    def id(self) -> Token:
        """Handles identifiers and reserved keywords.

        This method converts sequences of alphanumeric characters into 
        identifier tokens or reserved keyword tokens.

        Returns:
            Token: A token representing the identifier or reserved keyword.
        """
        token = Token(type=None, value=None, lineno=self.lineno, column=self.column)

        value = self.__get_multichar_by_condition(IS_ALPHANUMERIC)
        value_upper = value.upper()

        token_type = RESERVED_KEYWORDS.get(value_upper) if RESERVED_KEYWORDS.get(value_upper) else TokenType.ID

        if token_type is TokenType.BOOLEAN_CONST:
            value = True if value_upper == 'TRUE' else False

        elif value_upper == 'AND':
            token_type = TokenType.AND
            value = token_type.value
        elif value_upper == 'OR':
            token_type = TokenType.OR
            value = token_type.value
        elif value_upper == 'NOT':
            token_type = TokenType.NOT
            value = token_type.value
        
        token.type = token_type
        token.value = value

        return token
        
    def get_next_token(self) -> Token:
        """Tokenizes the input text, returning one token at a time.

        This method converts the input text into tokens, handling whitespace, 
        comments, identifiers, integers, operators, and other tokens.

        Returns:
            Token: The next token in the input text.
        """
        while self.current_char is not None:
            # Handle whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Handle comments
            if self.current_char == TokenType.COMMENT.value:
                self.advance()
                self.skip_comment()
                continue
            
            # Handle identifiers (functions / reserved keywords)
            if self.current_char.isalpha():
                return self.id()
            
            # Hanlde constant integers
            if self.current_char.isdigit():
                return self.integer()
            

            # Handle double-character tokens
            try:
                value = self.current_char + str(self.peek())
                token_type = TokenType(value)
            except ValueError:
                pass
            else:
                token = Token(
                    type = token_type,
                    value=value,
                    lineno=self.lineno,
                    column=self.column
                )
                self.advance()
                self.advance()
                return token
            

            # Handle single-character tokens
            try:
                token_type = TokenType(self.current_char)
            except ValueError:
                # Current char is not a defined single-character token
                self._error()
            else:
                token = Token(
                    type = token_type,
                    value=token_type.value,
                    lineno=self.lineno,
                    column=self.column
                )

                self.advance()
                return token
        
        # End-of-file (EOF) was reached
        return Token(type=TokenType.EOF, value=None)
