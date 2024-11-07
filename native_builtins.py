from value.value import Value
from value.types import *


def to_string(x: Value):
    if x.type == int_type:
        return x.value
    else:
        raise Exception(f"to-string not implemented for type {x.type.value}")

