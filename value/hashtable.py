from .types import hashtable_type
from .value import Value

def hashtable(dictionary):
    return Value(type=hashtable_type, value=dictionary)

