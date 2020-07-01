from tools import *
from astclass import *
from baseclass import *
from interpreter_type import *
from interpreter_value import *
from interpreter_show import *
from keywords import *
from parser import *
from lexer import *



def test():
    tests_list = [
        # (id, code_string, type_res, value_res)
        (1, "1 + 2 * 2 + 2;;", INT, 7),
        (2, "let a = ref 0 in while !a <> 4 do begin print_int !a; a := !a + 1 end done;;", UNIT, None),
        (3, "let i = ref 1 and n = 10 in while !i <> n do begin print_int !i; i := !i + 1 end done;;", UNIT, None),
    ]
    # Liste des erreurs rencontrées
    eroors_list = []
    for id, texte, type_expected, value_expected in tests_list:
        lexer = Lexer(texte)
        parser = Parser(lexer)
        node = parser.program()

        interpreter_type = InterpreterType(node)
        type_res = interpreter_type.interpret()

        interpreter_value = InterpreterValue(node)
        value_res = interpreter_value.interpret()

        if type_expected != type_res:
            eroors_list.append(f"Erreur got {type_res} instead of {type_expected} for test {id}")
        if value_expected != value_res:
            eroors_list.append(f"Erreur got {value_res} instead of {value_expected} for test {id}")
    if len(eroors_list) == 0:
        print(colors.OKGREEN, f"Tests: {len(tests_list)}/{len(tests_list)}", colors.ENDC)
    else:
        print(colors.FAIL, f"Tests: {len(tests_list) - len(eroors_list)}/{len(tests_list)}", colors.ENDC)
        error(*eroors_list)


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

#interpreter_show = InterpreterShow(node)
#interpreter_show.interpret()


interpreter_type = InterpreterType(node)
type_res = interpreter_type.interpret()
interpreter_value = InterpreterValue(node)
value_res = interpreter_value.interpret()


print(colors.OKBLUE, "Interpret result:", type_res, "-", value_res, colors.ENDC)

test()
