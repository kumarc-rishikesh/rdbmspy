from pyparsing import *
# Define the grammar elements

select_stmt = CaselessKeyword("select")
from_stmt = CaselessKeyword("from")
where_stmt = CaselessKeyword("where")
limit_stmt = Optional(CaselessKeyword("limit"))

# Define parser components
identifier = Word(alphas, alphanums + "_").setName("identifier")
column_name = Group(
    Suppress(Optional("(")) + 
    (Literal("*") | delimitedList(identifier, ",")) +
    Suppress(Optional(")"))
)
table_name = identifier
end_chars=one_of("limit ;", caseless=True)
condition_operator = oneOf("= != < >")
logical_operator = oneOf("AND OR")
# where_condition = Opt("(")+ Group(identifier + condition_operator + (quotedString | Word(nums))) + Opt(")")+ Opt(logical_operator)
where_condition = Opt("(")+ Group(identifier + condition_operator + (quotedString | identifier | Word(nums))) + Opt(")")+ Opt(logical_operator)
where_conditions = Optional(OneOrMore(where_condition),default=[])
limit_number = Optional(Word(nums),default=0)

# Define the structure of the SQL query
query = (select_stmt +
         column_name("columns") +
         from_stmt +
         table_name("table") +
         where_stmt +
         Group(where_conditions)("conditions") +
         limit_stmt +
         limit_number("limit") +
         Suppress(";"))

def parse_sql_query(input_string):
    try:
        parsed_data = query.parseString(input_string)
        return {
            "columns": parsed_data["columns"].asList(),
            "table": parsed_data["table"],
            "conditions": parsed_data["conditions"].asList(),
            "limit": parsed_data["limit"]
        }
    except Exception as e:
        print(f"Error parsing query: {e}")
        return {}

if __name__ == "__main__":
    print("To be used only for debugging!!! Run main instead")
    input_str=input("Input SQL string:\n")
    op=parse_sql_query(input_str)
    print(op)
