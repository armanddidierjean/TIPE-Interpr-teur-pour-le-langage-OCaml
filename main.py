from tools import *
from astclass import *
from baseclass import *
from interpreter_type import *
from interpreter_value import *
from keywords import *
from parser import *
from lexer import *



def test():
    erreurs = []
    for texte, type_expected, value in [(text1, INT, 3), (text2, INT, 3), (text3, UNIT, None), (text4, UNIT, None), (program, UNIT, None)]:
        lexer = Lexer(texte)
        parser = Parser(lexer)
        node = parser.program()

        interpreter_type = InterpreterType(node)
        type_res = interpreter_type.interpret()

        interpreter_value = InterpreterValue(node)
        value_res = interpreter_value.interpret()

        if type_expected != type_res:
            erreurs.append(f"Erreur got {type_res} instead of {type_expected} for test {texte}")
        if value != value_res:
            erreurs.append(f"Erreur got {value_res} instead of {value} for test {texte}")
    error(*erreurs)


text1="1+2;;"
text2 = "let a = ref 1 in begin a := 2; !a+1 end;;"
text3 = "let a = ref 0 in while !a <> 4 do begin print_int !a; a := !a + 1 end done;;"
text4 = "print_int 4;;"

texte = "let a = ref 1 in a + 1;;"

program = """
let i = ref 1 and n = 10 
    in 
        while !i <> n do 
            begin 
                print_int !i; 
                i := !i + 1 
            end 
        done;;"""

#lexer = Lexer(program)


#typer = Typer(node)
#typer.interpret()

math = "1 + 2 * 2 + 2;;"

lexer = Lexer(math)
parser = Parser(lexer)
node = parser.program()

interpreter_type = InterpreterType(node)
type_res = interpreter_type.interpret()
interpreter_value = InterpreterValue(node)
value_res = interpreter_value.interpret()


print(colors.OKBLUE, "Interpret result:", type_res, "-", value_res, colors.ENDC)

#test()