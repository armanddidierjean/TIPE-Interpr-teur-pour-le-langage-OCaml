from tools import *
from astclass import *
from baseclass import *
from interpreter_type import *
from interpreter_value import *
from interpreter_show import *
from keywords import *
from parser import *
from lexer import *



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
"""
text = "let f = fun a b c -> begin print_int 4; print_string b; c+a end in 5;;"

text="let a = 1+2 in a;;"
text = "let a = ref 0 in while !a <> 4 do begin print_int !a; a := !a + 1 end done;;"

text = "let f = fun a b () c -> 1 in f 1 begin print_int 2; 'test' end 3 4;;"

text = "let f = fun a b () c -> 1 in f 1 begin print_int 2; 'test' end 3 4 + 2;;"


text = "a+b;;"

text = "f 1 3 2;;"
"""

text = "let f = fun a b c -> begin print_int 4; print_string b; c+a end in f 3 'TEXT' 3;;"

text = "let f = fun a b () -> 1 in f 1 't' ();;"

text = "let f = fun a () c -> 1 in f 1 () 1;;"

text = """
let rec factorielle = fun n -> 
    if n = 1 
        then 1 
        else n * factorielle (n-1)
    in factorielle 6;;
"""

"""

let time f =
  let t = Unix.gettimeofday () in
  let res = f () in
  Printf.printf "Execution time: %f secondsn"
                (Unix.gettimeofday () -. t);
  res
;;

let time f x =
    let t = Sys.time() in
    let fx = f x in
    Printf.printf "Execution time: %fs\n" (Sys.time() -. t);
    fx;;

let rec fibo = fun n ->
    if n = 0
        then 0
        else if n = 1
            then 1
            else (fibo (n-1)) + (fibo (n-2))
            
        in time fibo 25;;


Pour n = 20

Sans loggin
 Interpret result: INT - 6765 
Downloaded the tutorial in 1.3433 seconds


Avec loggin
 Interpret result: INT - 6765 
Downloaded the tutorial in 12.9806 seconds

Pour n = 25, sans loggin

 Interpret result: INT - 75025 
Downloaded the tutorial in 15.5668 seconds

n = 25, natif
              Execution time: 0.003599s

"""

text = """
let rec fibo = fun n ->
    if n = 0
        then 0
        else if n = 1
            then 1
            else (fibo (n-1)) + (fibo (n-2))
    in
        fibo 25;;


"""

text = "let a b = b in begin print_int (a 1); a 'h' end;;"

import time
tic = time.perf_counter()

lexer = Lexer(text)
parser = Parser(lexer)
node = parser.program()




#interpreter_show = InterpreterShow(node)
#interpreter_show.interpret()


interpreter_type = InterpreterType(node)
type_res = interpreter_type.interpret()

print(type_res)



interpreter_value = InterpreterValue(node)
value_res = interpreter_value.interpret()

print(colors.OKBLUE, "Interpret result:", type_res, "-", value_res, colors.ENDC)

toc = time.perf_counter()

print(f"Downloaded the tutorial in {toc - tic:0.4f} seconds")

#test()

"""

# Function declaration
node = Program(Block(AssignmentStatement([AssignmentFunction("f", Function(["a"], [INT], PrintInt(Literal(3, INT))))], Block(Literal(4, INT)))))
# Function declaration and call
# -> UNIT
node = Program(Block(AssignmentStatement([AssignmentFunction("f", Function(["a"], [INT], PrintInt(Literal(3, INT))))], Block(FunctionCall("f", [Literal(1, INT)])))))
# -> INT
node = Program(Block(AssignmentStatement([AssignmentFunction("f", Function(["a"], [INT], Literal(3, INT)))], Block(FunctionCall("f", [Literal(1, INT)])))))
"""