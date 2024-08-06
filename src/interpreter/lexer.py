from .token import Token,TokenType,RESERVED_KEYWORDS
from .errors import LexerError

IS_ALPHABETIC = lambda char: char.isalpha()
IS_ALPHANUMERIC = lambda char: char.isalnum()
IS_NUMERIC = lambda char: char.isdigit()

class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.lineno = 1
        self.column = 1
    
    def _error(self) -> None:
        raise LexerError(
            "Lexer error on '{lexeme}' line: {lineno} column: {column}".format(
                lexeme = self.current_char,
                lineno= self.lineno,
                column = self.column
            )
        )
    
    def advance(self) -> None:
        """
        Advance the `pos` pointer and set the `current_char` variable.
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

    def advance_if_match(self, char:str) -> None:
        if self.current_char == char:
            self.advance()
        else:
            self._error()

    def peek(self) -> str:
        """
        Return the character at `self.pos + 1` without consuming it.
        """
        peek_pos = self.pos + 1

        return self.text[peek_pos] if peek_pos <= len(self.text) - 1 else None
    
    def peek_next_token(self) -> Token:
        origin_pos = self.pos
        origin_lineo = self.lineno
        origin_column = self.column

        token = self.get_next_token()
        self.pos = origin_pos
        self.lineno = origin_lineo
        self.column = origin_column
        self.current_char = self.text[origin_pos]

        return token
    
    def skip_whitespace(self) -> None:
        """
        Advance the `pos` pointer until the next non-whitespace character.
        """
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self) -> None:
        """
        Advance the `pos` pointer until the end of the comment line (i.e. new line).
        """
        while self.current_char != '\n':
            self.advance()
        self.advance()
    
    def __get_multichar_by_condition(self, condition) -> str:
        """
        Returns a full identifier (multi-digit number, reserved keyword, etc.) from `text` based on a `condition` function.
        """
        result = ''
        while self.current_char is not None and condition(self.current_char):
            result += self.current_char
            self.advance()
        
        return result

    def integer(self) -> Token:
        """
        Return a multi-digit poitive integer consumed from `text`.
        """
        token = Token(type=TokenType.INTEGER_CONST, value=None, lineno=self.lineno, column=self.column)

        result = self.__get_multichar_by_condition(IS_NUMERIC)

        token.value = int(result)

        return token
        
    def id(self) -> Token:
        """
        Handle identifiers (e.g. function call) and reserved keywords
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
        """
        Tokenizer (Lexican Analyzer) Method.

        The method converts the into into tokens, one token at a time.
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




        
        


        


