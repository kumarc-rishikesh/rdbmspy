# json_str = "[{ state: 'California', region: 'West', pop: 2312312321, pop_male: 3123123, pop_female: 123123 },{ state: 'Texas', region: 'South', pop: 100000, pop_male: 60000, pop_female: 40000 }]"
def get_inferred_schema(data):
    inferred_schema = {}
    for i in data[0].keys():
        if isinstance(data[0][i], float):
            inferred_schema[i] = "float"
        else:
            inferred_schema[i] = "str"
    return inferred_schema

def read_file_into_memory(filename):
    try:
        with open(filename, "r") as f:
            file_string = f.read()
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
        json_str=json_str.strip()
        for i in json_str[2:-3].split('},'):
            d={}
            for j in i[1:].split(","):
                key,val = j.split(":")
                key = key.strip().replace('"','').replace("'",'')
                val = val.strip().replace('"','').replace("'",'')
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
