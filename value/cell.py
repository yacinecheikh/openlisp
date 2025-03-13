from .types import cell_type
from .value import Value
from .unique import nil

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

def reverse(cell):
    result = nil
    while cell != nil:
        expr = car(cell)
        cell = cdr(cell)
        result = cons(expr, result)
    return result


def make_list(*args):
    result = nil
    for x in args:
        result = cons(x, result)
    return reverse(result)

def map_list(cell, f):
    result = nil
    while cell is not nil:
        head = car(cell)
        result = cons(f(head), result)
        cell = cdr(cell)
    return reverse(result)

