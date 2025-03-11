from .types import native_function_type, lisp_function_type, function_type
from . import keyword
from .cell import make_list, cons, car, cdr
from .value import Value


before_eval = keyword.keyword("before-eval")
after_eval = keyword.keyword("after-eval")
no_eval = keyword.keyword("no-eval")

def native_function(f, exec_mode=after_eval):
    native_func = Value(type=native_function_type, value=f)
    return Value(type=function_type, value=cons(exec_mode, native_func))

def lisp_function(arglist, body, env, exec_mode=after_eval):
    func_data = make_list(arglist, body, env)
    func = Value(type=lisp_function_type, value=func_data)
    return Value(type=function_type, value=cons(exec_mode, func))


def with_exec_mode(func, exec_mode):
    assert func.type == function_type
    func_data = cdr(func.value)
    return Value(function_type, cons(exec_mode, func_data))

def get_exec_mode(func):
    assert func.type == function_type
    return car(func.value)


def get_arglist(lisp_func):
    assert lisp_func.type == function_type
    func_data = cdr(lisp_func.value)
    assert func_data.type == lisp_function_type
    arglist = car(func_data.value)
    return arglist

def get_body(lisp_func):
    assert lisp_func.type == function_type
    func_data = cdr(lisp_func.value)
    assert func_data.type == lisp_function_type
    body = car(cdr(func_data.value))
    return body

def get_closure(lisp_func):
    assert lisp_func.type == function_type
    func_data = cdr(lisp_func.value)
    assert func_data.type == lisp_function_type
    env = car(cdr(cdr(func_data.value)))
    return env

