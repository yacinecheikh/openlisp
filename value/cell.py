from .types import cell_type
from .value import Value

def cons(car, cdr):
    return Value(type=cell_type, value=(car, cdr))

#def equal(a, b):
#    assert a.type == unique_type
#    assert b.type == unique_type
#    return a.value == b.value

def car(cell):
    assert cell.type == cell_type
    return cell.value[0]

def cdr(cell):
    assert cell.type == cell_type
    return cell.value[1]

