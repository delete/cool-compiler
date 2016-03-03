class Main inherits IO {
    c : Int <- 1;
    flag : Bool <- true;
    main() : Object { 
        {
            out_string("Hello, world.\n");
            (let countdown : Int <- 20 in
                while flag loop
                    {
                        countdown <- countdown - 1;
                        out_int(c);
                    }
                pool
            );
        }
    };
}; 
