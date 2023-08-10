import MnF_manipulation as module
 #  symmetric-rserveing-model 

def build_reserve_graph(m,n,x1) -> list:
    ''' Build one of two reserve graphs (its side functions) '''
    m_reserve = n - m + 1
    procs = []
    for i in range(n):
        procs.append(i+x1)
    return module.get_side_functions(m_reserve,n,procs,dual=True)

def build_main_graph(m,n,reserve_funcs,x1):
    ''' Build one of the two main graphs (its side functions) '''
    procs = []
    for i in range(n):
        procs.append(i+x1)
    j = 1
    for i in reserve_funcs:
        procs.append("g" + str(j))
        j+=1
    return module.get_side_functions(m+len(reserve_funcs),n+len(reserve_funcs),procs)

def replace_function_names(funcs,reserve_funcs) -> list:
    ''' Transform function names into their functions '''
    reserve_func_names = []
    j = 1
    for i in reserve_funcs:
        reserve_func_names.append("g" + str(j))
        j+=1
    result = []
    for symbol in funcs:
        if isinstance(symbol,list):
            result.append(replace_function_names(symbol,reserve_funcs))
        elif symbol in reserve_func_names:
            result.append(reserve_funcs[reserve_func_names.index(symbol)])
        else:
            result.append(symbol)
    return result

def build_model(m1,n1,m2,n2) -> tuple[list,list]:
    ''' Build model (tuple of lists of side functions), utilizes all functions from above '''
    reserve1 = build_reserve_graph(m1,n1,1)
    reserve2 = build_reserve_graph(m2,n2,n1+1)

    main1 = build_main_graph(m1,n1,reserve2,1)
    main2 = build_main_graph(m2,n2,reserve1,n1+1)

    funcs1 = replace_function_names(main1,reserve2)
    funcs2 = replace_function_names(main2,reserve1)

    return (funcs1,funcs2)

def test():
    j = 1
    k = 1

    print("\n--------------------------\n")
    for i in build_reserve_graph(3,7,11):
        print("g" + str(k) + str(j) + " = " + str(i))
        j+=1
    j = 1
    k+= 1
    print("\n--------------------------\n")
    for i in build_reserve_graph(5,10,1):
        print("g" + str(k) + str(j) + " = " + str(i))
        j+=1
    j = 1
    k = 1
    print("\n--------------------------\n")
    for i in build_main_graph(5,10,build_reserve_graph(3,7,11),1):
        print("f" + str(k) + str(j) + " = " + str(i))
        j+=1
    j = 1
    k+= 1
    print("\n--------------------------\n")
    for i in build_main_graph(3,7,build_reserve_graph(5,10,1),11):
        print("f" + str(k) + str(j) + " = " + str(i))
        j+=1
    j = 1
    k = 1
    print("\n--------------------------\n")
    for i in replace_function_names(build_main_graph(3,7,build_reserve_graph(5,10,1),11),build_reserve_graph(5,10,1)):
        print("f" + str(k) + str(j) + " = " + str(i))
        j+=1
    j = 1
    k = 1
    print("\n\n\n\n\n\n")
    for i in build_model(5,10,3,7)[0]:
        print("f" + str(k) + str(j) + " = " + str(i))
        j+=1
    j = 1
    k+= 1
    print("\n\n\n\n\n\n")
    for i in build_model(5,10,3,7)[1]:
        print("f" + str(k) + str(j) + " = " + str(i))
        j+=1
    j = 1
    k+= 1
    return build_model(5,10,3,7)