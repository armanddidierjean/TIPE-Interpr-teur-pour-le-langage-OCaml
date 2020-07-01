from baseclass import *
from keywords import *

#####################
#       Lexer       #
#####################
class Lexer:
    """
    Lexer: a OCaml Lexer

    Parameters
    ----------
    text : str
        string that will be executed

    Methods
    -------
    get_next_token()
        return the next token found in text
        return EOF when all tokens have been lexed
    """
    def __init__(self, text):
        self.text = text

        self.current_pos = -1
        self.current_char = None
        
        self.current_token = None

        # Generate the first character
        self.advance()

        #print("self.current_pos", self.current_pos, "self.current_char", self.current_char)

    def advance(self, nb=1):
        """
        Get next charactere from text:
         - modify self.current_pos
         - modify self.current_char

        If there is no nex characters, self.current_char is set to None

        Parameters
        ----------
        nb : int, optionnal
            Number of character to advance (default is 1)
        """
        for _ in range(nb):
            self.current_pos += 1
            if self.current_pos < len(self.text):
                self.current_char = self.text[self.current_pos]
            else:
                self.current_char = None

    def peek(self, nb=1):
        """
        Return the nb next charactere from text
        If there is no nex characters, return None

        Parameters
        ----------
        nb : int, optionnal
            Number of character to return (default is 1)
        """
        if self.current_pos + nb > len(self.text):
                return None
        result = ''
        for i in range(nb):
            result += self.text[self.current_pos + i]
        return result

    def get_id(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def get_number_token(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        if self.current_char is None or self.current_char != '.':
            return Token(INT, int(result))
        
        result += '.'
        self.advance()
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        return Token(FLOAT, int(result))

    def get_next_token(self):
        """
        Parse and return the next token found in text
        
        return EOF when all tokens have been parsed

        Raises
        ------
        SyntaxError
            If a not defined character is found
        """
        current_char = self.current_char
        #print("Getting next token, char=", self.current_char)

        if current_char is None:
            return Token(EOF, None)

        if self.current_char == ' ' or self.current_char == '\n' or self.current_char == '\t':
            # skip whitespace
            self.advance()
            return self.get_next_token()

        ############### NUMBER ###############
        if self.current_char.isdigit():
            return self.get_number_token()

        ############### ID ###############
        if self.current_char.isalpha() and self.current_char.islower():
            name = self.get_id()
            if name in RESERVED_KEYWORDS:
                return RESERVED_KEYWORDS[name]
            else:
                return Token(ID, name)

        ############### BINOP ###############
        if self.peek(2) == '+.':
            self.advance(2)
            return Token(PLUS_FLOAT, '+.')

        if current_char == '+':
            self.advance()
            return Token(PLUS_INT, '+')
        
        if self.peek(2) == '-.':
            self.advance(2)
            return Token(MINUS_FLOAT, '-.')

        if current_char == '-':
            self.advance()
            return Token(MINUS_INT, '-')
        
        if self.peek(2) == '*.':
            self.advance(2)
            return Token(MUL_FLOAT, '*.')

        if current_char == '*':
            self.advance()
            return Token(MUL_INT, '*')
        
        if self.peek(2) == '/.':
            self.advance(2)
            return Token(DIV_FLOAT, '/.')

        if current_char == '/':
            self.advance()
            return Token(DIV_INT, '/')
        
        ############### Micelianous ###############

        if current_char == '(':
            self.advance()
            return Token(LPAREN, '(')
        
        if current_char == ')':
            self.advance()
            return Token(RPAREN, ')')
        
        if current_char == ';':
            self.advance()
            return Token(SEMI, ';')

        if self.peek(2) == ':=':
            self.advance(2)
            return Token(REASSIGN, ':=')
        
        if self.peek(2) == '<>':
            self.advance(2)
            return Token(DIFFERENT, '<>')
        
        if current_char == '=':
            self.advance()
            return Token(EQUALS, '=')

        if current_char == '!':
            self.advance()
            return Token(EXCLAMATION, '!')

        raise SyntaxError("Invalid charactere")
