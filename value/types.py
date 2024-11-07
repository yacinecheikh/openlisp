from .value import Value

type_type = Value(type=None, value=None)
type_type.type = type_type
type_type.value = type_type

# data types
int_type = Value(type=type_type, value="int")
str_type = Value(type=type_type, value="str")
#array_type = Value(type=type_type, value=None)
hashtable_type = Value(type=type_type, value="hashtable")
keyword_type = Value(type=type_type, value="keyword")
unique_type = Value(type=type_type, value="unique")

# metaprogramming types
symbol_type = Value(type=type_type, value="symbol")
cell_type = Value(type=type_type, value="cell")

# function types
lisp_function_type = Value(type=type_type, value="lisp-function")
native_function_type = Value(type=type_type, value="native-function")
function_type = Value(type=type_type, value="function")




