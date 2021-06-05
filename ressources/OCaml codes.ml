let i = ref 1 and n = 10
    in 
        while !i <> n do 
            begin
                print_int !i;
                i := !i + 1
            end
        done;; 


let rec factorielle = fun n -> 
    if n = 1 
        then 1 
        else n * factorielle (n-1)
    in factorielle 6;;


let f n = n + 1;;