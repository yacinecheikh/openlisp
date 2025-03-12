"""
WARNING:
tests are sequential
(if one test fails, assume every tests after this one fail too)
(each test assumes the previous one to work and relies on that assumption)

"""


# *_type
from value.types import *
from value.symbol import symbol
from value.string import string
from value.integer import integer

from value.cell import cons
from value.environment import environment, bind
from value.unique import true, false, nil


def check_value(lisp_value, lisp_type, python_value):
    assert lisp_value.type == lisp_type
    assert lisp_value.value == python_value


def test_lookup():
    "lookup variables"
    from interpreter import lookup

    env = environment()
    bind(env, symbol("a"), integer(5))
    bind(env, symbol("x"), string("hi"))

    check_value(
        lookup(env, symbol("a")),
        int_type, 5
    )
    check_value(
        lookup(env, symbol("x")),
        str_type, "hi"
    )
    # undefined value
    assert lookup(env, symbol("y")) is None


def test_eval_simple():
    "evaluate simple atomic expressions"
    from interpreter import evaluate
    env = environment()
    bind(env, symbol("a"), integer(5))
    bind(env, symbol("x"), string("hi"))

    expr = symbol("a")
    result = evaluate(env, expr)
    check_value(result, int_type, 5)

    expr = integer(5)
    result = evaluate(env, expr)
    check_value(result, int_type, 5)

    expr = string("test")
    result = evaluate(env, expr)
    check_value(result, str_type, "test")


def test_compute_native():
    "compute a python-native function call (repr)"
    from value.cell import nil, cons

    from interpreter import compute, lookup
    from native_builtins import global_environment

    from utils import represent

    # scenario:
    # x = "some text"
    # assert (repr x) == represent(x)

    value = string("some text")
    expected = represent(value)

    env = environment()
    bind(env, symbol("x"), value)
    symb = symbol("x")
    args = cons(symb, nil)

    func = lookup(global_environment, symbol("repr"))

    result = compute(env, func, args)
    check_value(result, expected.type, expected.value)


def test_eval_define():
    pass


def test_compute_lisp():
    "compute a lisp-defined function call"
    from parse import read_all_expressions
    from native_builtins import represent

    # no need for incremental (read) here, read all expressions at once
    expressions = read_all_expressions(open("source/test/2-define.lisp").read())
    assert len(expressions) == 2
    define_expr, lambda_define_expr = expressions

    # safety check that the reader did its job
    assert represent(define_expr).value == "(define x 5)"
    assert represent(lambda_define_expr).value == "(define f (lambda (x) 5))"

    # test (define) first
    from native_builtins import global_environment
    from interpreter import evaluate, lookup

    result = evaluate(global_environment, define_expr)
    # (define) returns nil
    assert result is nil

    # lookup returns the correct value
    check_value(
            lookup(global_environment, symbol("x")),
            int_type, 5
    )

    result = evaluate(global_environment, lambda_define_expr)
    assert result is nil

    # compute the lambda
    from interpreter import compute
    f = lookup(global_environment, symbol("f"))
    # check the function definition
    assert f.type == function_type
    assert represent(f).value == "(lambda (x) 5)"


    # manually compute the function call from the global scope
    args = cons(integer(2), nil)
    result = compute(global_environment, f, args)
    check_value(result, int_type, 5)


def test_eval_lambda_calculus():
    "evaluate a lambda call"
    # ((lambda (x) x) 1) == 1
    from parse import next_expr
    from utils import represent
    from interpreter import evaluate
    from native_builtins import global_environment
    parsed, expr = next_expr("((lambda (x) x) 1)", 0)
    assert represent(expr).value == "((lambda (x) x) 1)"
    result = evaluate(global_environment, expr)
    check_value(result, int_type, 1)


def test_eval_funcall():
    "evaluate a function call"
    from native_builtins import global_environment
    from utils import represent
    from interpreter import evaluate
    from parse import read_all_expressions

    # define something
    define = "(define f (lambda (x) 5))"
    define_expr = read_all_expressions(define)[0]
    #assert represent(define_expr).value == define
    evaluate(global_environment, define_expr)

    source = "(f 2)"

    call_expr = read_all_expressions(source)[0]
    # safety checks
    assert represent(call_expr).value == "(f 2)"

    # do the eval
    result = evaluate(global_environment, call_expr)

    check_value(result, int_type, 5)


# load the code for the tests below
from parse import read_all_expressions
with open("source/test/3-compute.lisp") as f:
    source = f.read()
expressions = read_all_expressions(source)


def test_compute_semantics_0():
    assert len(expressions) == 5

def test_compute_semantics_1():
    "Run diverse scenarios to test runtime execution behavior"

    from native_builtins import global_environment
    from interpreter import evaluate, lookup
    from utils import represent

    expr = expressions[0]
    assert represent(expr).value == "(define f (lambda (x) x))"

    # define
    result = evaluate(global_environment, expr)
    #assert result is nil

    # call
    expr = read_all_expressions("(f 4)")[0]
    assert represent(expr).value == "(f 4)"
    result = evaluate(global_environment, expr)
    check_value(result, int_type, 4)

def test_compute_semantics_2():
    "Run diverse scenarios to test runtime execution behavior"

    from native_builtins import global_environment
    from interpreter import evaluate, lookup
    from utils import printval, represent

    # define
    #print("===define")
    expr = expressions[1]
    assert represent(expr).value == "(define f (lambda (x) nil))"
    result = evaluate(global_environment, expr)

    # inspect
    #print("===inspect")
    #func_expr = read_all_expressions("f")[0]
    #func = evaluate(global_environment, func_expr)
    #printval(func)

    # call
    #print("===call")
    call_expr = read_all_expressions("(f 3)")[0]
    result = evaluate(global_environment, call_expr)
    #printval(result)
    assert result is nil

def test_compute_semantics_3():
    "Run diverse scenarios to test runtime execution behavior"

    from native_builtins import global_environment
    from interpreter import evaluate, lookup
    from utils import printval, represent

    expr = expressions[2]
    evaluate(global_environment, expr)
    assert represent(lookup(global_environment, symbol("f"))).value == "(lambda () 2)"

    call = read_all_expressions("(f)")[0]
    check_value(
        evaluate(global_environment, call),
        int_type, 2
    )


def test_compute_semantics_4():
    "Run diverse scenarios to test runtime execution behavior"

    from native_builtins import global_environment
    from interpreter import evaluate, lookup
    from utils import printval, represent

    expr = expressions[3]
    assert represent(expr).value == "(define f (lambda (x y) y))"
    evaluate(global_environment, expr)

    call = read_all_expressions("(f 2 3)")[0]
    check_value(
        evaluate(global_environment, call),
        int_type, 3
    )


def test_compute_semantics_5():
    "Run diverse scenarios to test runtime execution behavior"

    from native_builtins import global_environment
    from interpreter import evaluate, lookup
    from utils import printval, represent

    from interpreter import compute

    # remove x and f from the environment
    del global_environment.value["x"]
    del global_environment.value["f"]

    expr = expressions[4]
    assert represent(expr).value == "(define f (lambda (x) (lambda nil x)))"
    evaluate(global_environment, expr)

    # call the first function and manually compute the second call
    call = read_all_expressions("(f 5)")[0]
    #printval(call1)
    lambda_result = evaluate(global_environment, call)
    #printval(result)
    # manually call the function
    result = compute(global_environment, lambda_result, args=nil)
    check_value(result, int_type, 5)

    # call both functions in a single expression
    call = read_all_expressions("((f 7))")[0]
    result = evaluate(global_environment, call)
    check_value(result, int_type, 7)


def test_macro():
    pass

def test_special():
    pass


def test_macroexpand():
    pass

