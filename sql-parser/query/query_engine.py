from .condition_eval import  conds_operator, res_operator, convert_to_postfix, eval_data
from .result import Result 

def run_where(inferred_schema, data_c,tq):
    #if no WHERE conditions, return the whole data
    if len(tq['conditions'][0])==0:
        return Result(data_c)
    #if only 1 condition, evaluate
    elif len(tq['conditions'])==1:
        cond=tq['conditions'][0]
        op, rej = conds_operator(data_c,cond[1],cond[0],cond[2],inferred_schema)
        return Result(op)
    # if 2 or more conditions, convert to postfix exression
    tokens=convert_to_postfix(tq['conditions'])
    mark = {"AND","OR", "and", "or"}
    stk = []
    f=0
    #evaluate postfix notation
    for x in tokens:
        if isinstance(x,str):
            if x in mark:
                b = stk.pop()
                a = stk.pop()

                res = eval_data(inferred_schema, data_c.copy(), x.upper() , a, b)
                stk.append(res)
                
        else:
            stk.append(x)
    return stk.pop()

def run_select(where_results,tq):
    op_arr=[]
    select_fields=tq['columns']
    #check if wildcard 
    if select_fields[0] == "*":
        return where_results

    #if not wildcard, get specified fields
    for row in where_results.data:
        op_json={}
        for field in select_fields:
            op_json[field] = row[field]
        op_arr.append(op_json)
    op = Result(op_arr)
    return(op)

def run_limit(select_results,tq):
    op_arr=[]
    dt=select_results.data
    limit = float(tq['limit'])
    #using limit 0 as dont limit
    if limit==0:
        return select_results
    else: 
        if len(dt)<=limit:
            return select_results
        else:
            i=0
            while i<limit:
                op_arr.append(dt[i])
                i+=1
    op = Result(op_arr)
    return op

def get_query_results( data, query, inf_schema ):
    #Following applicable SQL order of execution FWGHSOL : WHERE->SELECT->LIMIT 
    # print(data, query, inf_schema)
    tq = query
    data_copy = data.copy()
    # print(data_copy)
    where_results = run_where(inf_schema, data_copy, tq)
    select_results = run_select(where_results, tq)
    limit_results = run_limit(select_results, tq)

    return limit_results
