class Main inherits IO {
    c : Int <- 1;
    main() : Object { 
        {
            out_string("Hello, world.\n");
            out_int(c);
            let b : Int <- 1, 
                a : String <- "A" in
            { 
                out_string(a);
                out_string("==");
                out_int(b);
            };
        }
    };
}; 