from value import hashtable, unique, symbol, cell, keyword, function
from value.environment import environment
from value.types import *


def lookup(env, symbol):
    name = symbol.value
    bindings = env.value
    #print(name)
    #print(bindings)
    if name in bindings:
        return bindings[name]
    if bindings["parent-scope"] is not unique.nil:
        #print(name)
        #print(type(name))
        parent_scope = bindings["parent-scope"]
        return lookup(parent_scope, symbol)
    return None


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
        result = func_value.value(env, args)
    # TODO: function environment (closure + args)
    elif func_value.type is lisp_function_type:
        arglist = cell.car(func_value.value)
        body = cell.car(cell.cdr(func_value.value))
        closure_env = cell.car(cell.car(cell.cdr(func_value.value)))
        #print("closure:")
        #print(type(closure_env.value))
        #print(closure_env.value)


        # local environment definition
        local_env = environment(closure_env)
        #print("local:")
        #print(type(local_env.value))
        #print(local_env.value)
        # parameters
        argvals = args
        while arglist is not cell.nil:
            argname = cell.car(arglist)
            argval = cell.nil
            if argvals is not cell.nil:
                argval = cell.car(argvals)
                argvals = cell.cdr(argvals)
            arglist = cell.cdr(arglist)

            local_env.value[argname.value] = argval


        # form evaluation
        result = cell.nil
        while body is not cell.nil:
            expr = cell.car(body)
            body = cell.cdr(body)

            result = evaluate(local_env, expr)

    else:
        raise ValueError("Invalid function value; should not happen")


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
        head = cell.car(expr)
        args = cell.cdr(expr)
        func = evaluate(env, head)

        assert func.type is function_type

        return compute(env, func, args)
    else:
        return expr


# TODO: test evaluate for complex expressions (funcall, lists)






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


