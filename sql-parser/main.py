from read_json import read_file_into_memory, get_json_arr
from get_sql import parse_sql_query
from query_engine import get_query_results

import sys

if __name__ == '__main__':
    arguments = sys.argv[1:]
    file_loc = arguments[0]
    sql_str = input("Please input SQL statement:\n")
    try:
        json_str=read_file_into_memory(file_loc)
        json_arr, inferred_schema=get_json_arr(json_str)

        parsed_qry = parse_sql_query(sql_str)
        
        op = get_query_results(data = json_arr ,query = parsed_qry, inf_schema = inferred_schema)
        print(op.data)
        
    except Exception as e:
        print("There was an error")
        print("Error is :", e)
