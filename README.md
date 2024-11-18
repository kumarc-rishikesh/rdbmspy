An in-memory database that accepts JSON inputs & SQL queries , and returns the query result in the JSON format.
## Files
- main. py
- read_json.py
- get_sql.py
- query/query_engine.py
- query/condition_eval.py
- query/result. py

## Steps to run
```
1. nix develop
2. ./main.bin <path/to/input/json> (may take a while to buiild python binary)
	OR
2. python3 main.py <path/to/input/json>
```
or
```
1. Get Python version 3.11.8 and pyparsing version 3.0.9
2. python3 main.py <path/to/input/json>

there are two jsons to test with in test_jsons/
```
## JSON Parser

- The input json is in a non-traditional format hence I have written a parser to be able to read it from a file in module read_json.py
  Limitation : The parser dislikes special characters and will remove them. It expects an array of json enclosed in quotes.
- The file is first read into memory using the read_file_into_memory(), it then returns a string which is then parsed by get_json_arr
## SQL Parser
- For SQL parsing, I am using the pyparsing library. It returns a json of type:
	```
	columns :: [ String ]

	table :: String

	conditions :: [ Either String [String] ] (storing the “(“ and “AND”,”OR”operations to convert to) postfix later

	limit :: Int
	```
- I am not parsing the extra single quotes on the string to be able to differentiate it from a column name later on.
- This I believe is where Haskell’s/ PureScript’s type system would come in handy

## Query Executor

- I am going to follow the standard SQL execution : FWGHSOL : WHERE->SELECT->LIMIT(the three applicable here)
- Firstly I convert the infix WHERE statements to postfix to be able to evaluate it ( AST was also an option I know TextQL uses )  
- There are then 3 helper functions
	```
	1. get_str_val
	2. get_num_val
	3. loop_
	```
- The Where conditions are evaluated in the condition_eval module.
- I convert the infix WHERE conditions to postfix to be able to evaluate it ( AST was also an option I know TextQL uses )  

- There are a few functions here:

	1. get_str_val -> takes a string and returns either the string or the string in the attribute mentioned ( Ex : WHERE col1=’SomeString’ , WHERE col1 = col2 )
	2. convert_to postfix does as the name suggests and prec sets a precedence
	3. get_num_val -> takes an int and returns either the float or the float stored in the attribute mentioned ( Ex : WHERE col1=200 , WHERE col1 > col2 )
	4. conds_operator -> a function that takes a single query, and puts data into either
	5. good_data(passed the condition) or rejected_data ( keeping rejected_data just in case OR = NOT(A) ∩ B is more performant)
	6. Res_operator -> a function that takes two Result types and returns a single Result after evaluating either AND / OR
	7. eval_data -> calls either conds_operator or res_operator depending on the type of stack element
	8. run_where -> takes the postfix stack and evaluates the WHERE clauses accordingly
	9. run_select -> picks the keys required from the data and passes it on to
	10. run_liimit -> returns the final SQL output	

