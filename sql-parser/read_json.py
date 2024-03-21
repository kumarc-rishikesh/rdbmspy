from functools import reduce

#infer the schema of the json read. this comes in handy later on
def get_inferred_schema(data):
    inferred_schema = {}
    for i in data[0].keys():
        if isinstance(data[0][i], float):
            inferred_schema[i] = "float"
        else:
            inferred_schema[i] = "str"
    return inferred_schema

#reads the file into memory (streaming would have been better)
def read_file_into_memory(filename):
    try:
        with open(filename, "r") as f:
            file_string = f.read().strip()
        return file_string
    except Exception as e:
        print("File reading was unsuccessful")
        raise e

def get_json_arr(json_str):
    json_arr=[]
    try:
        #just a primitive check to make sure atleast 1 json exists
        json_str.index("[")
        json_str.index("]")
        json_str.index("{")
        json_str.index("}")
        json_arr=[]
        to_replace=['"',"'",'{','}','\n']
        json_str=json_str.strip()
        for i in json_str[2:-3].split('},'):
            d={}
            for j in i[1:].split(","):
                key,val = j.split(":")

                #getting rid of unneccessary characters in the key, val strings 
                key=reduce((lambda text, char: text.replace(char, '')), to_replace, key)
                key=key.strip().lower()
                val=reduce((lambda text, char: text.replace(char, '')), to_replace, val)
                val=val.strip()

                #store as float
                if val.isnumeric():
                    d[key]=float(val)
                else:
                    d[key]=val
            json_arr.append(d)

        inferred_schema = get_inferred_schema(json_arr)
        # print(inferred_schema)
        return (json_arr, inferred_schema)
        
    except Exception as e:
        print("JSON parsing was unsuccessful")
        raise e

if __name__ == '__main__':
    print("To be used only for debugging! Run main instead")
    json_str = read_file_into_memory(input())
    
    json_arr, inferred_schema = get_json_arr(json_str)
    print(json_arr,inferred_schema)
