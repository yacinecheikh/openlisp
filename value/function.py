from .types import native_function_type, lisp_function_type, function_type
from . import keyword
from .cell import make_list

before_eval = keyword.keyword("before-eval")
after_eval = keyword.keyword("after-eval")
no_eval = keyword.keyword("no-eval")

def native_function(f, exec_mode=after_eval):
    native_func = Value(type=native_function_type, f)
    return Value(type=function_type, cons(exec_mode, native_function))

def lisp_function(arglist, body, env, exec_mode=after_eval):
    func_data = make_list(arglist, body, env)
    func = Value(type=lisp_function_type, value=func_data)
    return Value(type=function_type, cons(exec_mode, func))
