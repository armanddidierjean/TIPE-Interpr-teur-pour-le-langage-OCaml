from tools import *
from astclass import *
from baseclass import *
#from interpreter_type import *
from interpreter_value import *
from keywords import *
from parser import *
from lexer import *


program = """
let i = ref 1 and n = 10 
    in 
        while !i <> n do 
            begin 
                print_int !i; 
                i := !i + 1 
            end 
        done;;"""

lexer = Lexer(program)
parser = Parser(lexer)
node = parser.program()

#typer = Typer(node)
#typer.interpret()

interpreter = Interpreter(node)

value = interpreter.interpret()

print(colors.OKBLUE, "Interpret result:", value, colors.ENDC)
