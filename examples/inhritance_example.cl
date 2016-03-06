class A inherits IO {

    hello(x: Int) : Object { 
        {            
            out_string("Hello, world.\n");
            out_int(x);
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
            a.hello(1);
        }
    };
}; 
