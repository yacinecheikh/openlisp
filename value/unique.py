from .types import unique_type
from .value import Value

def unique(label):
    return Value(type=unique_type, value=label)

def equal(a, b):
    assert a.type == unique_type
    assert b.type == unique_type
    return a.value == b.value

