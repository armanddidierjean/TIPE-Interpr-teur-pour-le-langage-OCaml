from baseclass import *
from keywords import *

#####################
#       Lexer       #
#####################
class Lexer:
    """
    OCaml Lexer

    Parameters
    ----------
    text : str
        string that will be tokenized

    Methods
    -------
    get_next_token()
        return the next token found in text
        return EOF when all the text have been lexed
    """

    # WARNING
    # All eating methods using while loop to find a specific character
    # should **always** check `self.current_char is not None`
    # to prevent an infinit loop may happen. 
    # OCaml example: `let a = 'text;;`

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
        Update the current charactere:
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
        If there is no next character return None

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
    
    def isEnd(self):
        """
        Return true if the end of text is attained
        """
        return self.current_char is None

    def isNotEnd(self):
        """
        Return not isEnd()
        """
        return not self.isEnd()

    def get_id(self):
        """
        Return an id: an alphanumeric string forming a word
        Accepted characters:
            a-z, A-Z, 1-9, _
        The function get_next_token will check the first character is a-Z, A-Z before calling this the method.
        """
        result = ''
        while self.isNotEnd() and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def get_number_token(self):
        """
        Return an INT or a FLOAT token 
        """
        # Note the position of the begining of the number for error reporting
        pos = self.current_pos

        result = ''
        while self.isNotEnd() and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        if self.isEnd() or self.current_char != '.':
            return Token(INT, int(result), pos, len(result))
        
        result += '.'
        self.advance()
        while self.isNotEnd() and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        return Token(FLOAT, float(result), pos, len(result))
    
    def get_string_token(self):
        """
        Return a string: a text delimited by two quotes or double quotes
        Support character escapement
        """
        # The delimiter can be a simple quote ' or a double quote "
        delimiter = self.current_char

        # Begin position of the string
        pos = self.current_pos

        # Pass the first delimiter
        self.advance()

        result = ''
        # We are expecting a second delimiter so we can suppose the string wont be finished before we found it
        while self.isNotEnd() and self.current_char != delimiter:
            # NOTE: currently \n and \t are not preserved
            # Escaped character: \" \' ...
            if self.current_char == '\\':
                # We just pass the backslash
                # then add the char even if it's the delimiter
                self.advance()
            result += self.current_char
            self.advance()
        
        # Make sure the remaining character is the delimiter
        if self.current_char == delimiter:
            # Pass the second delimiter
            self.advance()
            return Token(STRING, result, pos, len(result))
        else:
            # The code was entirely read but the string was not closed
            raise SyntaxError("The string was not closed")

    def pass_comment(self):
        """
        Advance in the text while the current char is inside a comment
        Nested comments are required to be each closed
        """
        # Pass the '(*'
        self.advance(2)
        while self.isNotEnd() and self.peek(2) != '*)':
            # Support nested comments
            if self.peek(2) == '(*':
                self.pass_comment()
            self.advance()
        
        # Make sure the remaining characters are a comment closer
        if self.peek(2) == '*)':
            # Pass the '*)'
            self.advance(2)
        else:
            raise SyntaxError("The comment was not closed")

    def get_next_token(self):
        """
        Parse and return the next token found in text
        Return EOF when all tokens have been parsed

        Raises
        ------
        SyntaxError
            If a not defined character is found
        """
        current_char = self.current_char
        current_pos = self.current_pos

        if current_char is None:
            return Token(EOF, None, -1, -1) # NOTE: we could use None instead of -1

        # Skip whitespace, new lines and tabs
        if self.current_char == ' ' or self.current_char == '\n' or self.current_char == '\t':
            self.advance()
            return self.get_next_token()

        # Skip comments
        if self.peek(2) == '(*':
            self.pass_comment()
            return self.get_next_token()

        ############### NUMBER ###############
        if self.current_char.isdigit():
            return self.get_number_token()
        
        ############### STRING ###############
        if self.current_char in ('"', "'"):
            return self.get_string_token()

        ########### ID or KEYWORDS ###########
        if self.current_char.isalpha() and self.current_char.islower():
            name = self.get_id()
            length = len(name)              # Length of the code
            if name in RESERVED_KEYWORDS:
                return Token(RESERVED_KEYWORDS[name], None, current_pos, len(name))
            else:
                return Token(ID, name, current_pos, length)

        ########### Two characters ###########
        if self.peek(2) == '->':
            self.advance(2)
            return Token(ARROW, '->', current_pos, 2)
            
        ############### BINOP ###############
        if self.peek(2) == '+.':
            self.advance(2)
            return Token(PLUS_FLOAT, '+.', current_pos, 2)

        if current_char == '+':
            self.advance()
            return Token(PLUS_INT, '+', current_pos, 1)
        
        if self.peek(2) == '-.':
            self.advance(2)
            return Token(MINUS_FLOAT, '-.', current_pos, 2)

        if current_char == '-':
            self.advance()
            return Token(MINUS_INT, '-', current_pos, 1)
        
        if self.peek(2) == '*.':
            self.advance(2)
            return Token(MUL_FLOAT, '*.', current_pos, 2)

        if current_char == '*':
            self.advance()
            return Token(MUL_INT, '*', current_pos, 1)
        
        if self.peek(2) == '/.':
            self.advance(2)
            return Token(DIV_FLOAT, '/.', current_pos, 2)

        if current_char == '/':
            self.advance()
            return Token(DIV_INT, '/', current_pos, 1)
        
        ############### Micelianous ###############

        if current_char == '(':
            self.advance()
            return Token(LPAREN, '(', current_pos, 1)
        
        if current_char == ')':
            self.advance()
            return Token(RPAREN, ')', current_pos, 1)
        
        if current_char == ';':
            self.advance()
            return Token(SEMI, ';', current_pos, 1)

        if self.peek(2) == ':=':
            self.advance(2)
            return Token(REASSIGN, ':=', current_pos, 2)
        
        if self.peek(2) == '<>':
            self.advance(2)
            return Token(DIFFERENT, '<>', current_pos, 2)
        
        if current_char == '=':
            self.advance()
            return Token(EQUALS, '=', current_pos, 1)

        if current_char == '!':
            self.advance()
            return Token(EXCLAMATION, '!', current_pos, 1)
        
        if self.peek(2) == '&&':
            self.advance(2)
            return Token(BOOLEANCONJUNCTION, '&&', current_pos, 2)
        
        if self.peek(2) == '||':
            self.advance(2)
            return Token(BOOLEANDISJUNCTION, '||', current_pos, 2)

        raise SyntaxError("Invalid charactere")
