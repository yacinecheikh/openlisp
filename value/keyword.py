from .types import keyword_type
from .value import Value


def keyword(x):
    return Value(type=keyword_type, value=x)

def equal(a, b):
    assert a.type == keyword_type
    assert b.type == keyword_type
    return a.value == b.value
