from .types import str_type
from .value import Value

def string(x):
    return Value(type=str_type, value=x)

