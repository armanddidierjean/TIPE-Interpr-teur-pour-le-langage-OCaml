from tools import *
from astclass import *
from baseclass import *
from interpreter_type import *
from interpreter_value import *
from interpreter_show import *
from keywords import *
from parser import *
from lexer import *

text = """
let rec factorielle = fun n -> 
    if n = 1 
        then 1 
        else n * factorielle (n-1)
    in factorielle 6;;
"""

lexer = Lexer(text)
parser = Parser(lexer)
node = parser.program()

interpreter_type = InterpreterType(node)
type_res = interpreter_type.interpret()

interpreter_value = InterpreterValue(node)
value_res = interpreter_value.interpret()

print(colors.OKBLUE, "Interpret result:", type_res, "-", value_res, colors.ENDC)