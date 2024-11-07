from .types import symbol_type
from .value import Value

def symbol(x):
    return Value(type=symbol_type, value=x)

def equal(a, b):
    assert a.type == symbol_type
    assert b.type == symbol_type
    return a.value == b.value

