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
        (4, "let a = ref 'hello world' in begin a := 'Hello World!'; print_string !a end;;", UNIT, None),
        (5, 'begin print_string "4\\"" (* print 4" (* then nested comments should work*) *); "Hello" end;;', STRING, "Hello"),
        (6, "let a = 'text' in let a = 3 in a;;", INT, 3),
    ]
    # Liste des erreurs rencontrées
    errors_list = []
    for id, texte, type_expected, value_expected in tests_list:
        lexer = Lexer(texte)
        parser = Parser(lexer)
        node = parser.program()

        print(" * Test", id)

        interpreter_type = InterpreterType(node)
        type_res = interpreter_type.interpret()

        interpreter_value = InterpreterValue(node)
        value_res = interpreter_value.interpret()

        if type_expected != type_res:
            errors_list.append(f"Erreur got {type_res} instead of {type_expected} for test {id}")
        if value_expected != value_res:
            errors_list.append(f"Erreur got {value_res} instead of {value_expected} for test {id}")
    if len(errors_list) == 0:
        print(colors.OKGREEN, "##############")
        print(f" # Tests: {len(tests_list)}/{len(tests_list)} #")
        print(" ##############", colors.ENDC)
    else:
        print(colors.FAIL, "##############")
        print(f" # Tests: {len(tests_list) - len(errors_list)}/{len(tests_list)} #")
        print(" ##############", colors.ENDC)
        error(*errors_list)


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

#text = "'text';;"

#text = "let a = ref 6 in 1;;"

#text = "let a = ref 't' in begin a := 'Text'; print_string !a end;;"
text = "let f = fun a b c -> begin print_int 4; print_string b; c+a end in 5;;"

lexer = Lexer(text)
parser = Parser(lexer)
node = parser.program()

interpreter_show = InterpreterShow(node)
interpreter_show.interpret()


interpreter_type = InterpreterType(node)
type_res = interpreter_type.interpret()

print(type_res)

"""
interpreter_value = InterpreterValue(node)
value_res = interpreter_value.interpret()

print(colors.OKBLUE, "Interpret result:", type_res, "-", value_res, colors.ENDC)

#test()
"""

# Function declaration
node = Program(Block(AssignmentStatement([AssignmentFunction("f", Function(["a"], [INT], PrintInt(Num(3, INT))))], Block(Num(4, INT)))))
# Function declaration and call
# -> UNIT
node = Program(Block(AssignmentStatement([AssignmentFunction("f", Function(["a"], [INT], PrintInt(Num(3, INT))))], Block(FunctionCall("f", [Num(1, INT)])))))
# -> INT
node = Program(Block(AssignmentStatement([AssignmentFunction("f", Function(["a"], [INT], Num(3, INT)))], Block(FunctionCall("f", [Num(1, INT)])))))
