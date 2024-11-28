from value.value import Value
from value.types import *
from value.unique import nil
from value.cell import car, cdr


from value import hashtable, unique, function


def environment(parent=unique.nil):
    bindings = {
        "parent-scope": parent,
    }
    lisp_value = hashtable.hashtable(bindings)
    bindings["current-scope"] = lisp_value
    return lisp_value


global_environment = environment()


def define_global(name, func, exec_mode=function.after_eval):
    bindings = global_environment.value
    # convert lisp cells to *args
    def f(arglist):
        args = []
        while arglist is not nil:
            args.append(car(arglist))
            arglist = cdr(arglist)
        return func(*args)
    wrapped_func = function.native_function(f, exec_mode)
    bindings[name] = wrapped_func
    return func


def builtin(name, exec_mode=function.after_eval):
    def decorator(func):
        return define_global(name, func, exec_mode)
    return decorator


#define_global("to-string", to_string)


#@builtin("+")
#def add(*args):
#    pass

@builtin("to-string")
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


@builtin("repr")
def represent(x: Value):
    if x.type in (int_type, symbol_type, cell_type):
        return to_string(x)
    if x.type == str_type:
        return Value(str_type, f'"{x.value}"')
    if x.type == hashtable_type:
        h = {}
        for key, val in x.value.items():
            if key == "current-scope" and val is x:
                continue
            h[key] = represent(val).value
        return Value(str_type, str(h))
    if x.type == unique_type:
        return Value(type=str_type, value=x.value)
    if x.type == function_type:
        exec_mode = car(x.value)
        func_val = cdr(x.value)
        return Value(str_type, f"<{exec_mode.value}> " + represent(func_val).value)
    if x.type == native_function_type:
        return Value(str_type, str(x.value))
    #if x.type == type_type:
    #    return 
    else:
        raise Exception(f"repr not implemented for type {x.type.value}")


@builtin("inspect")
def inspect(x: Value):
    string = represent(x)
    if x.start_position is not None:
        string.value += f" at {x.start_line}:{x.start_position}-{x.end_line}:{x.end_position}"
    return string


@builtin("quote", exec_mode=function.no_eval)
def quote(x: Value):
    return x


# quasiquote
# if
# define
# lambda
# and or
