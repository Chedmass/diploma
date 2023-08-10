import math
 #  model-transmutation-and-function-manipulation
def split_model_into_parts(m,n,x1=1,x2=0):
    ''' Splits model (K) into two parts with different or same m and n parameters '''
    result = []
    if x2 == 0:
        x2 = n
    if m < n:
        K1 = (m,math.ceil(n/2),x1,x1+math.ceil(n/2)-1)
        K2 = (m,math.floor(n/2),x1+math.ceil(n/2),x2)
        result.append((K1,K2))
        othersK1 = split_model_into_parts(K1[0],K1[1],K1[2],K1[3])
        othersK2 = split_model_into_parts(K2[0],K2[1],K2[2],K2[3])
        if othersK1:
            for i in othersK1:
                result.append(i)
        if othersK2:
            for i in othersK2:
                result.append(i)
        return result
    else:
        return False

def main_function(K1,K2,main=False):
    result = [] 
    ''' Forms and returns function, calculated by main function.
    (f1,f2 ... = [(1,k1,k2),(2,k1,k2)...] where k1,k2 = (m,n,x1,x2)) '''

    i = K1[0] - 1
    j = K1[3]

    while True:
        if i > 0:
            if main:
                value = (j,(K1[0]-i,K1[1],K1[2],K1[3]),(i,K2[1],K2[2],K2[3]))
            else:
                value = (K1[0]-i,K1[1],K1[2],K1[3]),(i,K2[1],K2[2],K2[3])
            if K1[0]-i <= K1[1] and i <= K2[1]:
                result.append(value)
        i -= 1
        j -= 1
        if i <= 0:
            break
    if len(result) > 0:
        return result
    return False

def edge_function(m,n,procs,x1=1,main=False,dual=False):
    ''' Forms and returns function,calculated by adge-case functions.
    (if m==n, if m==1, if m==n==1) '''
    if dual:
        operators = ["v","^"]
    else:
        operators = ["^","v"]
    func = []
    if m == 1:
        func.append(str(procs[x1-1]))
        for j in range(1,n):
            func.append(operators[0])
            func.append(str(procs[x1+j-1]))
    elif n == m:
        func.append(str(procs[x1-1]))
        for j in range(1,n):
            func.append(operators[1])
            func.append(str(procs[x1+j-1]))
    else:
        return False
    if main:
        return (x1,func)
    else:
        return (func)
    
def function_simplifying(K1,K2,procs,dual=False):
    ''' Forms functions from child-functions '''

    simplified = (function_part_simplifying(K1[0],K1[1],K1[2],K1[3],procs,dual=dual),function_part_simplifying(K2[0],K2[1],K2[2],K2[3],procs,dual=dual))

    result = []
    for symbol in simplified[0]:
        result.append(symbol)
    if dual:
        result.append("^")
    else:
        result.append("v")
    if simplified[1]:
        for symbol in simplified[1]:
            result.append(symbol)
    return result

def function_part_simplifying(m,n,x1,x2,procs,dual=False):
    ''' Forms functions from child-functions '''
    result = []

    func = edge_function(m,n,procs,x1=x1,dual=dual)
    if func:
        return func

    divided = split_model_into_parts(m,n,x1=x1,x2=x2)
    if not divided:
        return False
    for pair in divided:
        funcs = main_function(pair[0],pair[1])
        if funcs:
            for func in funcs:
                f = []
                K1 = function_part_simplifying(func[0][0],func[0][1],func[0][2],func[0][3],procs,dual=dual)
                K2 = function_part_simplifying(func[1][0],func[1][1],func[1][2],func[1][3],procs,dual=dual)
                for symbol in K1:
                    f.append(symbol)
                if dual:
                    f.append("^")
                else:
                    f.append("v")
                if K2:
                    for symbol in K2:
                        f.append(symbol)
                
                result.append(f)
        for part in pair:
            func = edge_function(part[0],part[1],procs,x1=part[2],dual=dual)
            if func:
                result.append(func)
    
    return result

def conj_insertion(func,dual=False):
    ''' Transforms default-type function into dual-type functions (changes operators to opposite) '''
    result = []
    last = None
    for i in func:
        if last == None:
            result.append(i)
            last = i
            continue
        if isinstance(last,list) and isinstance(i,list):
            if dual:
                result.append("v")
            else:
                result.append("^")
            result.append(conj_insertion(i,dual=dual))
            last = i
            continue
        if isinstance(i,list):
            result.append(conj_insertion(i,dual=dual))
            last = i
            continue
        result.append(i)
    return result

def get_side_functions(m,n,procs,dual=False):
    ''' Utilises other functions to build list of side functions for some GLM graph '''
    
    func = edge_function(m,n,procs,dual=dual)

    if func:
        return [func]

    N = n - m + 1

    vectorF = []
    for x in range(N):
        vectorF.append(None)

    dividedModel = split_model_into_parts(m,n)
    
    allf = []
    for pair in dividedModel:
        funcs = main_function(pair[0],pair[1],main=True)
        if funcs:
            allf.append(funcs)
        for part in pair:
            func = edge_function(part[0],part[1],procs,x1=part[2],main=True,dual=dual)
            if func:
                allf.append(func)

    for bracket in allf:
        if isinstance(bracket,list):
            for func in bracket:
                vectorF[int(func[0])-1] = function_simplifying(func[1],func[2],procs,dual=dual)
        else:
            vectorF[int(bracket[0])-1] = bracket[1]
    result = []
    for function in vectorF:
        result.append(conj_insertion(function,dual=dual))
    return result