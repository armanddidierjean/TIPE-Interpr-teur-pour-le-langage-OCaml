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
        (7, "let f = fun a b c -> begin print_int 4; print_string b; c+a end in f 3 'TEXT' 3;;", INT, 6),
        (8, "let f = fun a b () -> 1 in f 1 't' ();;", INT, 1),
        (9, "();;", UNIT, None)
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
            errors_list.append(f"#{id} types error: got {type_res} instead of {type_expected}")
        if value_expected != value_res:
            errors_list.append(f"#{id} value error: got {value_res} instead of {value_expected}")
    if len(errors_list) == 0:
        print(colors.OKGREEN, "┌────────────────────┐")
        print(f" │ Running tests:     │")
        print(f" │                {len(tests_list)}/{len(tests_list)} │")
        print(" └────────────────────┘", colors.ENDC)
    else:
        print(colors.FAIL, "┌────────────────────┐")
        print(f" │ Running tests:     │")
        print(f" │                {len(tests_list) - len(errors_list)}/{len(tests_list)} │")
        print(" └────────────────────┘", colors.ENDC)
        error(*errors_list)

test()

