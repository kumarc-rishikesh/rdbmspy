from .result import Result

def get_str_val(d,v):
    #check to see if the string is a string or a key
    if "'" in v:
        return v[1:-1]
    # if key, return the value ofthe key 
    elif v.lower() in d.keys():
        return d[v]
    else:
        raise Exception("Invalid Value")

def get_num_val(d,v):
    # if numeric then it is a number
    if v.isnumeric():
        v=float(v)
        
    elif "'" in v:
        raise Exception("Expected Number Got string")

    #if it is a key, get the value of the key and return
    elif v.lower() in d.keys():
        if isinstance(d[v], float):
            v=float(d[v])
        else:
            raise Exception("Expected Number Got string")
    else:
        raise Exception("invalid value")

    return v

#AND takes precedence over OR in SQL
def prec(con):
    if con == "OR" or con == "or":
        return 1
    elif con == "AND" or con == "and":
        return 2
    else:
        return 0

#infix to postfix
def convert_to_postfix(conds):
    result=[]
    stk=[]
    for i in range(len(conds)):
        con=conds[i]
        if isinstance(con,list):
            result.append(con)
        elif con =="(":
            stk.append(con)
        elif con == ")":
            while stk and stk[-1]!="(":
                result.append(stk.pop())
            stk.pop()
        else:
            while stk and prec(conds[i]) < prec(stk[-1]) or prec(conds[i]) == prec(conds[-1]):
                result.append(stk.pop())
            stk.append(con)
    while stk:
        result.append(stk.pop())
    return result


#takes a single query and loops through the database seperating it into records that satisfy condition and records that dont
def conds_operator(dc, cond, k, v, inf_schema):
    i = 0
    l = len(dc)
    rej_dc = []
    if l == 0:
        return (dc, rej_dc)

    # make sure only floats gets all 4 oerations
    if inf_schema[k] == "float":
        v = get_num_val(dc[i], v)
    else:
        if cond == "<" or cond == ">":
            raise Exception("only = and != operations supported for string fields")
        # print(dc[i])
        v = get_str_val(dc[i], v)

    # get all values that satisfy and do not satisfy the condition
    if cond == "<":
        while i < l:
            if dc[i][k] >= v:
                rej_dc.append(dc.pop(i))
                l -= 1
            else:
                i += 1
    if cond == ">":
        while i < l:
            # print(dc[i][k])
            if dc[i][k] <= v:
                rej_dc.append(dc.pop(i))
                l -= 1
            else:
                i += 1
    if cond == "=":
        while i < l:
            if dc[i][k] != v:
                rej_dc.append(dc.pop(i))
                l -= 1
            else:
                i += 1 
    if cond == "!=":
        while i < l:
            if dc[i][k] == v:
                rej_dc.append(dc.pop(i))
                l -= 1
            else:
                i += 1
    return (dc, rej_dc)

#performs AND/OR between two sets or data
def res_operator(ip_arr, x):
    op_arr=[]
    intersect_arr=[]
    good1, good2 = ip_arr[0].data, ip_arr[1].data
    # print(good1,good2)
    if x == "OR":
        # get the union of two sets of data
        for i in good1:
            if i in good2:
                intersect_arr.append(i)
            else:
                op_arr.append(i)
        for i in good2:
            if i in good1:
                if i not in intersect_arr:
                    intersect_arr.append(i)
            else:
                op_arr.append(i)
    else:
        # AND
        # get the intersection of two sets of data 
        for i in good1:
            if i in good2:
                intersect_arr.append(i)
        for i in good2:
            if i in good1 and i not in intersect_arr:
                intersect_arr.append(i)
    op_arr+=intersect_arr
    op = Result(op_arr)
    return op


#takes two arguents from the postfix stack and evaluates them
def eval_data(inferred_schema, data_c, x, a, b):
    res_arr=[]
    # print("x--------------------x")
    # print(a,b,x)
    # print("----------------------")

    #checking to see if a is a Result or a condition
    if isinstance(a,Result):
        res_arr.append(a)
    else:
        # if not a Result, get Result
        good, rej = conds_operator( data_c.copy() , a[1], a[0], a[2], inferred_schema)
        op = Result(good)
        res_arr.append(op)

    #checking to see if b is a Result or a condition
    if isinstance(b,Result):
        res_arr.append(b)
    else:
        good, rej = conds_operator( data_c.copy() , b[1], b[0], b[2], inferred_schema)
        op = Result(good)
        res_arr.append(op)
    return res_operator(res_arr, x)
