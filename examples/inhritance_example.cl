class A inherits IO {

    hello() : Int { 
        {
            out_int(1);
        }
    };
}; 


class Main inherits IO {
    i : Int <- 1;
    a : A <- new A;
    main() : Object { 
        {
            out_string("Hello, world.\n");
            out_int(i);
            a.hello();
        }
    };
}; 
