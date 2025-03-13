"""
WARNING:
tests are sequential
(if one test fails, assume every tests after this one fail too)
(each test assumes the previous one to work and relies on that assumption)
"""


# stdout capturing context manager:

from io import StringIO 
import sys

class capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout





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


"""
Run diverse scenarios to test runtime execution behavior
"""


# load the code for the tests below
from parse import read_all_expressions
with open("source/test/3-compute.lisp") as f:
    source = f.read()
expressions = read_all_expressions(source)


def test_compute_semantics_0():
    assert len(expressions) == 5

def test_compute_semantics_1():

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


"""
macros, specials and ahead-of-time macro expansion
"""


with open("source/test/4-macro.lisp") as f:
    source = f.read()

# read all expressions at once because the reader is not modified
meta_expressions = read_all_expressions(source)

# read expressions one by one (to follow the correct execution flow)
#from parse import next_expr
#position = 0
#while True:
#    position, expression = next_expr(source, position)
#    if expression is None:
#        break

from utils import printval, represent
from interpreter import evaluate, expand, lookup
from native_builtins import global_environment

def test_metaprogramming_1():
    "test keywords"
    assert len(expressions) == 5

    expr = meta_expressions[0]

    printval(expr)
    assert represent(expr).value == '(define no-eval (kw "no-eval"))'
    evaluate(global_environment, expr)
    result = lookup(global_environment, symbol("no-eval"))
    check_value(result, keyword_type, "no-eval")

def test_metaprogramming_2():
    "define a special"
    expr = meta_expressions[1]

    printval(expr)
    evaluate(global_environment, expr)
    result = lookup(global_environment, symbol("my-quote"))
    assert represent(result).value == "(function :no-eval (lambda (x) x))"


def test_metaprogramming_3():
    "run a special function with unevaluated arguments"
    expr = meta_expressions[2]

    printval(expr)
    result = evaluate(global_environment, expr)
    check_value(result, symbol_type, "x")

def test_metaprogramming_4():
    "define a macro with compile-time print and code generation"
    expr = meta_expressions[3]

    printval(expr)
    evaluate(global_environment, expr)
    result = lookup(global_environment, symbol("my-macro"))
    assert represent(result).value == '(function :before-eval (lambda () (print "macro expansion") (my-quote (print "generated code"))))'

# TODO: expand the macro before evaluating its result

# test expand

def test_metaprogramming_5():
    "test (expand)"

    import interpreter
    interpreter.debug = False

    expr = read_all_expressions("(print 5)")[0]
    #printval(expr)
    with capturing() as output:
        expanded = expand(global_environment, expr)
    assert represent(expanded).value == represent(expr).value
    # nothing printed
    assert str(output) == "[]"

    expr = meta_expressions[4]
    assert represent(expr).value == "(my-macro)"

    with capturing() as output:
        expanded = expand(global_environment, expr)
    assert represent(expanded).value == '(print "generated code")'
    # expanding the macro prints a message while generating code
    assert str(output) == "['macro expansion']"

    with capturing() as output:
        result = evaluate(global_environment, expanded)
    # executing the expanded code prints another message
    assert str(output) == "['generated code']"

    interpreter.debug = True



def test_metaprogramming_6():
    "expand a macro inside a loop"

    expr = meta_expressions[5]
    assert represent(expr).value == "(for (i (range 10)) (my-macro) 5)"

    import interpreter
    interpreter.debug = False

    with capturing() as output:
        expanded = expand(global_environment, expr)
    assert str(output) == "['macro expansion']"
    assert represent(expanded).value == '(for (i (range 10)) (print "generated code") 5)'


    with capturing() as output:
        result = evaluate(global_environment, expanded)
    expected = ["generated code"] * 10
    assert str(output) == str(expected)
    check_value(result, int_type, 5)

    interpreter.debug = True



