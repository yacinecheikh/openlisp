from .types import hashtable_type, str_type
from .value import Value

def hashtable(dictionary):
    return Value(type=hashtable_type, value=dictionary)

def setkey(table: Value, string: Value, value: Value):
    assert table.type == hashtable_type
    assert string.type == str_type

    table.value[string.value] = value

