from value.value import Value
from value.types import *
from value.unique import nil, true, false
from value.cell import car, cdr, make_list
from value.symbol import symbol
from value.keyword import keyword
from value.environment import environment, global_environment, bind
from value import function


from interpreter import evaluate

from utils import represent, to_string, printval

# interpreter.debug
import interpreter



def define_global(name, func, exec_mode=function.after_eval):
    bindings = global_environment.value
    # convert lisp cells to *args
    def f(env, arglist):
        args = []
        while arglist is not nil:
            args.append(car(arglist))
            arglist = cdr(arglist)
        return func(*args)
    # used for (repr)-ing python builtins
    f.__name__ = func.__name__
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
    # used for (repr)-ing python builtins
    f.__name__ = func.__name__
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

# constants
bind(global_environment, symbol("true"), true)
bind(global_environment, symbol("false"), false)
bind(global_environment, symbol("nil"), nil)

# functions (need to construct a function Value)
builtin("to-string")(to_string)
builtin("repr")(represent)

@builtin("print")
def print_value(x: Value):
    print(to_string(x).value)
    return nil

#@builtin("+")
#def add(*args):
#    pass



@builtin("quote", exec_mode=function.no_eval)
def quote(x: Value):
    return x


@special_builtin("define")
def define(env, symbol, expr):
    if interpreter.debug:
        print("(define):")
        print("call env:")
        printval(env)
        print("define expr:")
        printval(expr)
    assert symbol.type is symbol_type
    value = evaluate(env, expr)
    global_environment.value[symbol.value] = value
    return nil


@special_builtin("lambda")
def lambda_constructor(env, arglist, *body_forms):
    if interpreter.debug:
        print("(lambda):")
        print("call/closure env:")
        printval(env)
        print("lambda arg list:")
        printval(arglist)
    body = make_list(*body_forms)
    if interpreter.debug:
        print("lambda body:")
        printval(body)
    lisp_function = function.lisp_function(arglist, body, env, function.after_eval)
    return lisp_function

@special_builtin("for")
def for_loop(env, loop_params, *body_forms):
    if interpreter.debug:
        print("(for):")


@builtin("kw")
def keyword_constructor(s):
    assert s.type == str_type
    return keyword(s.value)

@builtin("function")
def function_constructor(exec_mode, func):
    """example: (function (keyword "no-eval") (lambda (x) x))"""
    if interpreter.debug:
        print("calling (function)")
    assert func.type == function_type
    assert exec_mode.type == keyword_type
    return function.with_exec_mode(func, exec_mode)



# quasiquote
# if
# and or
# gensym

