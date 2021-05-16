from baseclass import *
from keywords import *

#####################
#       Lexer       #
#####################
class Lexer:
    """
    Lexer: an OCaml Lexer

    Parameters
    ----------
    text : str
        string that will be tokenized

    Methods
    -------
    get_next_token()
        return the next token found in text
        return EOF when all tokens have been lexed
    """
    def __init__(self, text):
        self.text = text

        # Current character and its position in text
        self.current_pos = -1
        self.current_char = None
        
        self.current_token = None

        # Generate the first character
        self.advance()

    def advance(self, nb=1):
        """
        Get next charactere from text:
         - modify self.current_pos
         - modify self.current_char

        If there is no next character, self.current_char is set to None

        Parameters
        ----------
        nb : int, optional
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
        Return the nb next characters from text
        If there is no next characters, return None

        Parameters
        ----------
        nb : int, optional
            Number of character to return (default is 1)
        """
        if self.current_pos + nb > len(self.text):
                return None
        result = ''
        for i in range(nb):
            result += self.text[self.current_pos + i]
        return result

    def get_id(self):
        """
        Return an id: an alphanumeric string forming a word
        Accepted characters:
            a-z, A-Z, 1-9, _
        The function get_next_token will check the first character is a-Z, A-Z before calling this one.
        """
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def get_number_token(self):
        """
        Return an INT or a FLOAT token 
        """
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
        
        return Token(FLOAT, float(result))
    
    def get_string_token(self):
        """
        Return a string
        Support various string delimitation and character escape
        """
        delimiter = self.current_char
        # Pass the first delimiter
        self.advance()
        result = ''
        # We are expecting a second delimiter so we can suppose the string wont be finished before
        while self.current_char != delimiter:
            # Escaped character: \" \n...
            if self.current_char == '\\':
                # We just pass the backslash
                # The body of the while loop while add the char even if it's the delimiter
                self.advance()
            result += self.current_char
            self.advance()
        
        # Pass the second delimiter
        self.advance()

        return Token(STRING, result)

    def pass_comment(self):
        """
        Advance in the text while the current char is inside a comment
        """
        # Pass the '(*'
        self.advance(2)
        while self.peek(2) != '*)':
            # Support nested comments
            if self.peek(2) == '(*':
                self.pass_comment()
            self.advance()
        # Pass the '*)'
        self.advance(2)

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

        if current_char is None:
            return Token(EOF, None)

        if self.current_char == ' ' or self.current_char == '\n' or self.current_char == '\t':
            # skip whitespace or new lines and tabs
            self.advance()
            return self.get_next_token()

        if self.peek(2) == '(*':
            self.pass_comment()
            return self.get_next_token()

        ############### NUMBER ###############
        if self.current_char.isdigit():
            return self.get_number_token()
        
        ############### STRING ###############
        if self.current_char in ('"', "'"):
            return self.get_string_token()

        ############### ID ###############
        if self.current_char.isalpha() and self.current_char.islower():
            name = self.get_id()
            if name in RESERVED_KEYWORDS:
                return RESERVED_KEYWORDS[name]
            else:
                return Token(ID, name)

        ############### Two characters ###############
        if self.peek(2) == '->':
            self.advance(2)
            return Token(ARROW, '->')
            
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
        
        if self.peek(2) == '&&':
            self.advance(2)
            return Token(BOOLEANCONJUNCTION, '&&')
        
        if self.peek(2) == '||':
            self.advance(2)
            return Token(BOOLEANDISJUNCTION, '||')

        raise SyntaxError("Invalid charactere")
