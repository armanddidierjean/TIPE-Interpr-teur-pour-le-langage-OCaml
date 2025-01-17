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
        (1, "1 + 2 * 2 + 2;;", BUILTIN_TYPES["int"], 7),
        (2, "let a = ref 0 in while !a <> 4 do begin print_int !a; a := !a + 1 end done;;", BUILTIN_TYPES["unit"], None),
        (3, "let i = ref 1 and n = 10 in while !i <> n do begin print_int !i; i := !i + 1 end done;;", BUILTIN_TYPES["unit"], None),
        (4, "let a = ref 'hello world' in begin a := 'Hello World!'; print_string !a end;;", BUILTIN_TYPES["unit"], None),
        (5, 'begin print_string "4\\"" (* print 4" (* then nested comments should work*) *); "Hello" end;;', BUILTIN_TYPES["string"], "Hello"),
        (6, "let a = 'text' in let a = 3 in a;;", BUILTIN_TYPES["int"], 3),
        (7, "let f = fun a b c -> begin print_int 4; print_string b; c+a end in f 3 'TEXT' 3;;", BUILTIN_TYPES["int"], 6),
        (8, "let f = fun a b () -> 1 in f 1 't' ();;", BUILTIN_TYPES["int"], 1),
        (9, "();;", BUILTIN_TYPES["unit"], None),
        (10, "1 + 2 * (1 + 1) * 3;;", BUILTIN_TYPES["int"], 13),
        (11, "let rec factorielle = fun n -> if n = 1 then 1 else  n * factorielle (n-1) in factorielle 6;;", BUILTIN_TYPES["int"], 720),
        (12, "let f a b () = 1 in f 1 't' ();;", BUILTIN_TYPES["int"], 1),
        (13, "let rec factorielle n = if n = 1 then 1 else  n * factorielle (n-1) in factorielle 6;;", BUILTIN_TYPES["int"], 720),
        (14, ";;", BUILTIN_TYPES["unit"], None),
        (15, "- 1 + 1;;", BUILTIN_TYPES["int"], -2),          # Unary Op, !right associative!
        (16, "1 - 1 + 1;;", BUILTIN_TYPES["int"], 1),         # Binary Op
        (17, "let f a = a in begin f 1; f 'i' end;;", BUILTIN_TYPES["string"], 'i'),
        (18, "let a b = b in begin print_int (a 1); a 'h' end;;", BUILTIN_TYPES["string"], 'h'),
    ]
    # Liste des erreurs rencontrées
    errors_list = []
    # UNIT testing: on vérifie que le code est compilable
    # INTEGRATION testing on vérifie que le résultat est correct
    errorsManager.empty()
    for id, texte, type_expected, value_expected in tests_list:

        lexer = Lexer(texte)
        parser = Parser(lexer)
        node = parser.program()

        # Gestion des erreurs de parsing
        for errorItem in errorsManager.get():
            errors_list.append(f"#{id} parse error: {errorItem}")
        errorsManager.empty()

        interpreter_type = InterpreterType(node)
        type_res = interpreter_type.interpret()

        # Gestion des erreurs de l'interpreteur de type
        for errorItem in errorsManager.get():
            errors_list.append(f"#{id} interpreter type error: {errorItem}")
        errorsManager.empty()

        interpreter_value = InterpreterValue(node)
        value_res = interpreter_value.interpret()

        # Gestion des erreurs de l'interpreteur de valeur
        for errorItem in errorsManager.get():
            errors_list.append(f"#{id} interpreter value error: {errorItem}")
        errorsManager.empty()

        # Gestion des erreurs de type et valeur du résultat
        if type_expected != type_res:
            errors_list.append(f"#{id} types error: got {type_res} instead of {type_expected}")
        if value_expected != value_res:
            errors_list.append(f"#{id} value error: got {value_res} instead of {value_expected}")
        
    if len(errors_list) == 0:
        print(colors.OKGREEN, "┌──────────────────────┐")
        print(f" │ Running tests:       │")
        print(f" │                {len(tests_list)}/{len(tests_list)} │")
        print(" └──────────────────────┘", colors.ENDC)
    else:
        print(colors.FAIL, "┌──────────────────────┐")
        print(f" │ Running tests:       │")
        print(f" │                {len(tests_list) - len(errors_list)}/{len(tests_list)} │")
        print(" └──────────────────────┘", colors.ENDC)
        error(*errors_list)

test()

def errors_test():
    tests_list = [
        # (id, code_string, error_descrition)
        (1, "'text;;", 'Unclosed string'),
        (2, "(* first (* second *)", "Unclosed comment"),
        (3, "}", "Invalid character"),
        (4, "1", "Unterminated code"),
        (5, "let f a b = if true then a else b in f 1 'a';;", "Type error in function call and not in definition"),
    ]

    for test in tests_list:
        # An error is expected to occurs
        try:
            lexer = Lexer(test)
        except:
            pass

errors_test()   # Should silently pass
