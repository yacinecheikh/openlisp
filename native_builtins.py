from value.value import Value
from value.types import *
from value.unique import nil
from value.cell import car, cdr


# (to-string)
def to_string(x: Value):
    if x.type == int_type:
        return Value(str_type, str(x.value))
    elif x.type == str_type:
        return x
    elif x.type == symbol_type:
        return Value(str_type, x.value)
    elif x.type == cell_type:
        result = "("
        # while not nil
        while x != nil:
            head = car(x)
            x = cdr(x)
            result += represent(head).value
            if x != nil:
                result += " "
        result += ")"
        return Value(str_type, result)
    else:
        raise Exception(f"to-string not implemented for type {x.type.value}")


# (repr)
def represent(x: Value):
    if x.type in (int_type, symbol_type, cell_type):
        return to_string(x)
    if x.type == str_type:
        return Value(str_type, f'"{x.value}"')
    else:
        raise Exception(f"repr not implemented for type {x.type.value}")


# (inspect)
def inspect(x: Value):
    string = represent(x)
    if x.start_position is not None:
        string.value += f" at {x.start_line}:{x.start_position}-{x.end_line}:{x.end_position}"
    return string


