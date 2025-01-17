from value.value import Value
from value.types import *
from value.unique import nil, true, false
from value.cell import car, cdr, make_list
from value.environment import environment, global_environment
from value import function


from interpreter import evaluate



def define_global(name, func, exec_mode=function.after_eval):
    bindings = global_environment.value
    # convert lisp cells to *args
    def f(env, arglist):
        args = []
        while arglist is not nil:
            args.append(car(arglist))
            arglist = cdr(arglist)
        return func(*args)
    wrapped_func = function.native_function(f, exec_mode)
    bindings[name] = wrapped_func
    return func

# define special global
def define_special(name, func):
    bindings = global_environment.value
    # convert lisp cells to *args
    def f(env, arglist):
        args = []
        while arglist is not nil:
            args.append(car(arglist))
            arglist = cdr(arglist)
        return func(env, *args)
    wrapped_func = function.native_function(f, exec_mode=function.no_eval)
    bindings[name] = wrapped_func
    return func


def builtin(name, exec_mode=function.after_eval):
    def decorator(func):
        return define_global(name, func, exec_mode)
    return decorator

def special_builtin(name):
    def decorator(func):
        return define_special(name, func)
    return decorator


#define_global("to-string", to_string)

global_environment.value["true"] = true
global_environment.value["false"] = false
global_environment.value["nil"] = nil


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
    elif x.type == lisp_function_type:
        arglist = car(x.value)
        arglist_repr = represent(arglist).value
        body = car(cdr(x.value))
        body_repr = represent(body).value[1:-1]
        return Value(str_type, f"(lambda {arglist_repr} {body_repr})")
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


@special_builtin("define")
def define(env, symbol, expr):
    assert symbol.type is symbol_type
    value = evaluate(env, expr)
    global_environment.value[symbol.value] = value
    return nil


@special_builtin("lambda")
def lambda_constructor(env, arglist, *body_forms):
    body = make_list(*body_forms)
    lisp_function = function.lisp_function(arglist, body, env, function.after_eval)
    return lisp_function



# quasiquote
# if
# and or
# gensym

