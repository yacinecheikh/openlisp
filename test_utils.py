"""
test printing utilities (repr and to-string)

creates and manipulate lisp values to inspect them, but does not execute lisp code
"""


from utils import represent, to_string, printval

# datatype constructors
from value.integer import integer
from value.string import string
from value.symbol import symbol
from value.keyword import keyword
from value.unique import true, false, nil

from value.cell import make_list, car, cdr
from value.environment import environment, global_environment
from value.hashtable import hashtable
from value.function import (
    native_function, lisp_function,
    after_eval, no_eval, before_eval,

    get_exec_mode, with_exec_mode,
    get_arglist, get_body, get_closure
)

from value import types


env = environment()
env.value["x"] = integer(5)
env2 = environment(env)

# native function
def print_string(x):
    print(x.value)
native_func = native_function(print_string, exec_mode=after_eval)

# lisp function
# (lambda (y) x) defined with x as a closure, tagged as a normal function (:after-eval)
arglist = make_list(symbol("y"))
body = make_list(symbol("x"))
lisp_func = lisp_function(arglist, body, env2, exec_mode=before_eval)




values = [
    integer(5),
    string("test"),
    symbol("x"),
    keyword("kw"),
    nil,
    make_list(*(integer(x) for x in range(10))),
    hashtable({}),
    hashtable({"a": integer(3)}),
    env2,

    native_func,
    lisp_func,

    # test function manipulation utilities
    get_exec_mode(native_func),
    with_exec_mode(native_func, no_eval),
    get_arglist(lisp_func),
    get_body(lisp_func),
    get_closure(lisp_func),

]

repred = [
    "5", "\"test\"", "x", ":kw", "nil",
    "(0 1 2 3 4 5 6 7 8 9)",
    "(dict)",
    """\
(dict
      :a 3)""",
    """\
(dict
      :parent-scope (dict
                          :parent-scope nil
                          :x 5))""",

    "<native function print_string>",
    "(function :before-eval (lambda (y) x))",


    ":after-eval",
    "(function :no-eval <native function print_string>)",
    "(y)",
    "(x)",
    """\
(dict
      :parent-scope (dict
                          :parent-scope nil
                          :x 5))"""
]


def test_repr():
    assert len(values) == len(repred)
    for lisp_value, python_string in zip(values, repred):
        #printval(lisp_value)
        #print(python_string)
        assert python_string == represent(lisp_value).value

# TODO: not as critical as (repr)
def test_tostring():
    pass
