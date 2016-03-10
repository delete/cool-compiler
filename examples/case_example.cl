class A {};
class B inherits A {};
class C inherits B {};

class D {};

class Main inherits IO {
    var : B <- (new B);

   class_type(var : Object) : SELF_TYPE {        
        case var of
            a : A => out_string("Class type is now A\n");
            b : B => out_string("Class type is now B\n");
            c : C => out_string("Class type is now C\n");
            o : Object => out_string("Oooops\n");
        esac
   };

    main() : Object { 
        {            
            class_type(var);
        }
    };
}; 


