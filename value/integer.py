from .types import int_type
from .value import Value

def integer(i):
    return Value(type=int_type, value=i)

