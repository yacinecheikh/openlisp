from utils import represent, to_string

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
    after_eval, no_eval, before_eval
)

from value import types


env = environment()
env.value["x"] = integer(5)
env2 = environment(env)

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

    # TODO: create native function
    # TODO: lisp function
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
                          :x 5))"""
]


def test_repr():
    assert len(values) == len(repred)
    for lisp_value, python_string in zip(values, repred):
        #print(represent(lisp_value).value)
        #print(python_string)
        assert python_string == represent(lisp_value).value

def test_tostring():
    assert False
