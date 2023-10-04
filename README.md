# diploma
Diploma program
    The object of development is the software implementation of algorithms for building a symmetric system of GL-model models and its edge functions, the software implementation of the analysis of the built model for its effectiveness and validity at certain values of the state of the processors.

GL-Model
    Gl-Model is a representation of complex multiprocessor system. In this representation system state (working or failed) is represented by graph connectivity. Graph sides have functions assigned to them, these functions are logical, and use processor states as variables, if function output is False, then this side is no longer included in graph and may break graph connectivity, which would mean that system has failed. 
    In this case GL-Model represents a pair of multiprocessor systems, which can borrow some amount of processors from each other in case of high amount of failed processors, because both these systems can borrow processors, this GL-Model is called a symmetric <donor-recipient> GL-Model.

Side functions
    Side functions are formed from a set of variables, representing processor states, according to pre-defined algorithm with some rules:
     Main algorithm:
      - Define the model K(m,n), where variables m and n represent the fault tolerance and number of processors in system (sub-system) accordingly.
      - Split the model into two sub-models K1(m,n1) and K2(m,n2). These sub-models use processor variables from different ranges (e.g. if the model is K(m,7), then K1 would use first ceiling(n/2) variables, in this case form 1 to 4, and K2 would use the rest 5 to 7 (ceil(n/2)+1 to n))
      - Calculate all side functions for each sub-model and if possible, split first sub-model.
     Function building algorithm:
     
      If K1(m,n1)
      - Iterate variable j, from m-1 to 1. Each iteration is a separate function, each function numerated from m to 1:
      fm = K1(1,n1) v K2(m-1,n2)
      fm-1 = K1(2,n1) v K2(m-2,n2)
      ...
      f1 = K1(m-1,n1) v K2(1,n2)
        Where K2 is the second sub-module, fromed on splitting module K(m,n) in two sub-modules.
        Operator v is logical disjunction
      - These functions contain sub-modules, which will be recursively solved untill they match edge case functions.
     Edge case functions:
      - K(1,1):
       f1 = x1
      
      - K(1,n):
       f1 = x1;
       f2 = x2;
       ...
       fn = xn;
       also can be percieved as:
       f1 = x1 ^ x2 ^ ... ^ xn;
       (only in case if it's inside sub-module, formed by function building algorithm)
       (operator ^ is logical conjunction)
      
      - K(n,n):
       f1 = x1 v x2 v ... v xn

Model building
    In order to build GL-Model of this type, sets of processors are used to form two dual graphs, which will act as reserve graphs for other sub-system. Dual graphs are built the same way as usual ones, except logical operators, they are reversed, meaning, where would be conjunction will be disjunction and vise-versa.
    As the reserve graphs are built, the main graphs of sub-systems can be built, using each systems' processor variables and other system's reserve graph side functions as processor variables, after building these graphs, the reserve graph side functions are unfolded inside main graph side functions.
![DPpic1](https://github.com/Chedmass/diploma/assets/69762254/ef6e9e4f-b5b0-4489-a565-9b997bab9a92)
Implementation
   The program is splitted into three modules:
    MnF_manipulation - builds and transforms side functions
    SR_Model_builder - builds GL-Model of symmetrical <donor-recipient> type
    main - invokes test function
    
   Functions are implemented as lists of characters and recursively lists of characters.
    Test function returns sets of:
     - side functions of both reserve graphs
     - side functions of both main graphs with folded variables (from reserve graph, e.g. g11, g21 etc.)
     - side functions of both main graphs with unfolded variables
