from .types import unique_type
from .value import Value

def unique(label):
    return Value(type=unique_type, value=label)


nil = unique("nil")
true = unique("true")
false = unique("false")

