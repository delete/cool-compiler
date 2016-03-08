class A inherits IO {
    a : Int <- 2;
    hello(x: Int) : Int { 
        {            
            out_int(x);
            0;
        }
    };
}; 

class B inherits A {
    do() : String {
        {
            hello(2);
            out_int(a);
            "do nothing";
        }
    };
};

class Main inherits IO {
    i : Int <- 1;
    b : B <- new B;
    main() : Object { 
        {
            out_string("Hello, world.\n");
            out_int(i);
            b.do();
            b.hello(3);
        }
    };
}; 
