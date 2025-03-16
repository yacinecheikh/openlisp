from value import hashtable, unique, symbol, cell, keyword, function
from value.environment import environment, bind
from value.types import *
from value.function import (
    get_exec_mode,
    get_raw_function,

    get_arglist,
    get_body,
    get_closure,
)

from utils import printval, represent

# print each step of code execution
debug = True


def lookup(env, symbol):
    name = symbol.value
    bindings = env.value
    if debug:
        print("lookup:")
        printval(symbol)
        print("environment:")
        printval(env)
        if bindings["parent-scope"] is unique.nil:
            print("(no parent scope found)")
        else:
            print("(parent scope found)")
    #print(name)
    #print(bindings)
    if name in bindings:
        if debug:
            print("found! value: ", end="")
            printval(bindings[name])
        return bindings[name]
    if bindings["parent-scope"] is not unique.nil:
        #print(name)
        #print(type(name))
        parent_scope = bindings["parent-scope"]
        return lookup(parent_scope, symbol)
    return None



def compute(call_env, func, args):
    """
    Compute a function call ran in the current scope

    (f a b c)
    where f can be a python function or (arglist body closure_environment)
    f = list(arglist, body, func_env)

    to compute a lisp function:
    -create a local environment {parent=closure_environment a=arg1 b=arg2 c=arg3}
    -for expression in body:
        -evaluate expression in the local environment
    -return the last computed value (nil by default)

    in addition:
    if f is a function (:after-eval): evaluate arguments before computing the function call
    if f is a macro (:before-eval): evaluate the result of the function
    if f is special (:no-eval): do nothing (evaluation is done manually)

    """
    exec_mode = get_exec_mode(func)
    raw_function = get_raw_function(func)

    if raw_function.type is native_function_type:
        if debug:
            print("===================computing python function:", represent(func).value)
        # python functions get raw access to the current call environment
        result = raw_function.value(call_env, args)
    elif raw_function.type is lisp_function_type:
        if debug:
            print("===================computing lisp function:", represent(func).value)
        arglist = get_arglist(func)
        if debug:
            print("params:")
            printval(arglist)
            print("args:")
            printval(args)
        body = get_body(func)
        closure_env = get_closure(func)
        if debug:
            print("closure env:")
            printval(closure_env)
        assert closure_env.type is hashtable_type

        # local environment definition
        local_env = environment(closure_env)
        # parameters
        argvals = args
        while arglist is not cell.nil:
            argname = cell.car(arglist)
            argval = cell.nil
            if argvals is not cell.nil:
                argval = cell.car(argvals)
                argvals = cell.cdr(argvals)
            arglist = cell.cdr(arglist)

            bind(local_env, argname, argval)


        if debug:
            print("local environment:")
            printval(local_env)


        # form evaluation
        result = cell.nil
        while body is not cell.nil:
            expr = cell.car(body)
            body = cell.cdr(body)

            result = evaluate(local_env, expr)

    else:
        raise ValueError("Invalid function value; should not happen")

    return result



def expand(env, expr):
    """
    if g is a defined macro: (defmacro g ...)
    then:
    (f (g (h 5)))
    (g (h 5)) gets expanded
    """

    if debug:
        print("expanding: ", end="")
        printval(expr)

    # do not process cases other than (<symbol> ...)
    if expr.type is not cell_type:
        if debug:
            print("nothing to expand")
        return expr
    head = cell.car(expr)
    args = cell.cdr(expr)
    # try to expand the current (head . tail) form
    # if ok -> recursion
    # else -> expand sub-expressions
    if head.type is symbol_type:
        if debug:
            print("looking up the head of the list: ", end="")
            printval(head)
        f = lookup(env, head)
        # if f is a known (defined) macro
        if f is not None and f.type is function_type and keyword.equal(get_exec_mode(f), function.before_eval):
            if debug:
                print("found a macro expression!")
            expanded = compute(env, f, args)
            # keep expanding
            return expand(env, expanded)
    # did not expand the head (not a (macro ...) form)
    # -> expand sub-expressions
    if debug:
        print("could not find an expandable macro expression; expanding sub-expressions")
    expanded = cell.map_list(expr, lambda elt: expand(env, elt))
    return expanded



def evaluate(env, expr):
    """
    5 "test" -> return
    x -> lookup
    (a b (c)) -> expand; (evaluate parameters?); compute; (evaluate the result?)
    """
    if expr.type is symbol_type:
        result = lookup(env, expr)
        if result is None:
            raise ValueError(f"Symbol '{expr.value} is undefined")
        return result
    elif expr.type is cell_type:
        head = cell.car(expr)
        args = cell.cdr(expr)
        func = evaluate(env, head)

        assert func.type is function_type
        # function ? -> evaluate arguments
        # macro ? -> error
        # special ? do not evaluate
        exec_mode = get_exec_mode(func)
        if keyword.equal(exec_mode, function.after_eval):
            # function -> evaluate arguments
            args = cell.map_list(args, lambda arg: evaluate(env, arg))

        # macros should not be called at runtime
        assert not keyword.equal(exec_mode, function.before_eval)

        return compute(env, func, args)
    else:
        return expr


