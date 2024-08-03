from .token import Token,TokenType,RESERVED_KEYWORDS
from .errors import LexerError

class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.lineno = 1
        self.cloumn = 1
    
    def error(self) -> None:
        raise LexerError(
            "Lexer error on '{lexeme}' line: {lineno} column: {column}".format(
                lexeme = self.current_char,
                lineno= self.lineno,
                column = self.cloumn
            )
        )
    
    def advance(self) -> None:
        """
        Advance the `pos` pointer and set the `current_char` variable.
        """

        if self.current_char == '\n':
            self.lineno +=1
            self.cloumn = 0

        self.pos += 1

        # Check if EOF was reached, else extract the next char
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            self.cloumn += 1

    def peek(self) -> str:
        """
        Return the character at `self.pos + 1` without consuming it.
        """
        peek_pos = self.pos + 1

        return self.text[peek_pos] if peek_pos <= len(self.text) - 1 else None
    
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
        while self.current_char is not None and condition():
            result += self.current_char
            self.advance()
        
        return result

    def _integer(self) -> Token:
        """
        Return a multi-digit poitive integer consumed from `text`.
        """
        result = self.__get_multichar_by_condition(self.current_char.isdigit)
        # while self.current_char is not None and self.current_char.isdigit():
        #     result += self.current_char
        #     self.advance()

        return Token(
            type=TokenType.INTEGER_CONST,
            value=int(result),
            lineno=self.lineno,
            column=self.cloumn
        )
        
    def _id(self) -> Token:
        """
        Handle identifiers (e.g. function call) and reserved keywords
        """

        value = self.__get_multichar_by_condition(self.current_char.isalnum).upper()

        # value = ''
        # while self.current_char is not None and self.current_char.isalnum():
        #     value += self.current_char
        #     self.advance

        token_type = RESERVED_KEYWORDS.get(value) if RESERVED_KEYWORDS.get(value) else TokenType.ID

        if token_type is TokenType.BOOLEAN_CONST:
            value = True if value == 'TRUE' else False

        return Token(
            type=token_type,
            value=value,
            lineno=self.lineno,
            column=self.cloumn
        )
    
    def peek_next_token(self) -> Token:
        origin_pos = self.pos
        token = self.get_next_token()
        self.pos = origin_pos

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
            if self.current_char == TokenType.COMMENT:
                self.advance()
                self.skip_comment()
                continue

            # Handle identifiers (functions / reserved keywords)
            if self.current_char.isalpha():
                return self._id()
            
            # Hanlde constant integers
            if self.current_char.isdigit():
                return self._integer()
            
            # Handle single-character tokens
            try:
                token_type = TokenType(self.current_char)
            except ValueError:
                # Current char is not a defined single-character token
                self.error()
            else:
                token = Token(
                    type = token_type,
                    value=token_type.value,
                    lineno=self.lineno,
                    column=self.cloumn
                )

                self.advance()
                return token
        
        # End-of-file (EOF) was reached
        return Token(type=TokenType.EOF, value=None)




        
        


        


