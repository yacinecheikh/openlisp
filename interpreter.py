from value import hashtable, unique, symbol, cell, keyword, function
from native_builtins import represent, global_environment
from value.types import *


def environment(parent=unique.nil):
    bindings = {
        "parent-scope": parent,
    }
    lisp_value = hashtable.hashtable(bindings)
    bindings["current-scope"] = lisp_value
    return lisp_value



def lookup(env, symbol):
    name = symbol.value
    bindings = env.value
    if name in bindings:
        return bindings[name]
    if bindings["parent-scope"] is not unique.nil:
        parent_scope = bindings["parent-scope"]
        return lookup(parent_scope, symbol)
    return None


"""
from value import integer, string
env = environment()
env.value["a"] = integer.integer(5)
env.value["x"] = string.string("hi")

print(represent(lookup(env, symbol.symbol("a"))).value)
print(represent(lookup(env, symbol.symbol("x"))).value)
print(lookup(env, symbol.symbol("y")))
"""


#def compute_native(


#def lisp_function(arglist, body, env, exec_mode=after_eval):

def compute(env, func, args):
    """
    (f a b c)
    f = list(arglist, body, func_env)
    local_env = {(func_env)}
    for arg in args:
        local_env[arglist[0]] = a

    for expr in body:
    """
    exec_mode = cell.car(func.value)
    func_value = cell.cdr(func.value)
    # if function
    if keyword.equal(exec_mode, function.after_eval):
        args = cell.map_list(args, lambda arg: evaluate(env, arg))

    if func_value.type is native_function_type:
        result = func_value.value(*args)
    # TODO: function environment (closure + args)
    elif func_value.type is lisp_function_type:
        pass
    else:
        raise ValueError("Invalid function value; should not happen")
    argnames = cell.car(func_value)
    ### TODO: compute form or call
    # result
    result = nil


    if keyword.equal(exec_mode, function.before_eval):
        result = evaluate(env, result)
    return result



def expand(env, expr):
    """
    (defmacro g ...)
    (f (g (h 5)))
    """
    pass


def evaluate(env, expr):
    """
    5 "test" -> return
    x -> lookup
    (a b (c)) -> expand; (evaluate parameters?); compute; (evaluate the result?)
    """
    if expr.type is symbol_type:
        return lookup(env, expr)
    elif expr.type is cell_type:
        raise NotImplementedError
    else:
        return expr


# TODO: test evaluate for complex expressions (funcall, lists)
"""
from value import integer, string
env = environment()
env.value["a"] = integer.integer(5)
env.value["x"] = string.string("hi")


for expr in [symbol.symbol("a"), integer.integer(5), string.string("test")]:
    result = evaluate(env, expr)
    string = represent(result)
    print(string.value)
"""






##### lexical binding example
"""
(defun g ()
        (let ((counter 0))
          (lambda (x)
            (setf counter (+ counter x))
             counter)))


(defvar increment-counter (g))
(increment-counter 5)
"""


