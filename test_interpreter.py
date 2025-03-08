"""
WARNING:
tests are sequential
(if one test fails, assume every tests after this one fail too)
(each test assumes the previous one to work and relies on that assumption)

"""


def test_lookup():
    from value import integer, string, symbol
    from native_builtins import environment
    from interpreter import lookup

    env = environment()
    env.value["a"] = integer.integer(5)
    env.value["x"] = string.string("hi")

    assert lookup(env, symbol.symbol("a")).value == 5
    assert lookup(env, symbol.symbol("x")).value == "hi"
    assert lookup(env, symbol.symbol("y")) is None


def test_eval_simple():
    from value import integer, string, symbol, types
    from native_builtins import environment
    from interpreter import evaluate
    env = environment()
    env.value["a"] = integer.integer(5)
    env.value["x"] = string.string("hi")


    expr = symbol.symbol("a")
    result = evaluate(env, expr)
    assert result.type == types.int_type
    assert result.value == 5

    expr = integer.integer(5)
    result = evaluate(env, expr)
    assert result.type == types.int_type
    assert result.value == 5

    expr = string.string("test")
    result = evaluate(env, expr)
    assert result.type == types.str_type
    assert result.value == "test"


def test_compute_native():
    from value import string, cell, symbol, types
    from interpreter import compute
    from native_builtins import environment, global_environment
    from native_builtins import represent
    env = environment()
    env.value["x"] = string.string("test")
    symb = symbol.symbol("x")
    args = cell.cons(symb, cell.nil)

    #print(represent(global_environment).value)

    func = global_environment.value["repr"]

    result = compute(env, func, args)
    assert result.type == types.str_type
    assert result.value == '"test"'


def test_compute_lisp():
    from parse import read_all_expressions
    from native_builtins import represent

    expressions = read_all_expressions(open("source/test/2-define.lisp").read())
    assert len(expressions) == 2
    simple_define_expr, lambda_define_expr = expressions

    assert represent(simple_define_expr).value == "(define x 5)"
    assert represent(lambda_define_expr).value == "(define f (lambda (x) 5))"

    # evaluate the defines
    from native_builtins import global_environment
    from interpreter import evaluate
    result = evaluate(global_environment, simple_define_expr)

    #print(represent(global_environment).value)

    result = evaluate(global_environment, lambda_define_expr)
    #print(represent(global_environment).value)

    # compute the lambda
    from interpreter import lookup, compute
    from value import symbol, cell, integer
    from value.types import int_type
    f = lookup(global_environment, symbol.symbol("f"))
    args = cell.cons(integer.integer(2), cell.nil)
    # manual compute call
    result = compute(global_environment, f, args)
    #print(represent(result).value)
    assert result.type == int_type
    assert result.value == 5


def test_eval_funcall():
    from value.types import int_type
    from native_builtins import global_environment, represent
    from interpreter import evaluate
    from parse import read_all_expressions

    source = "(f 2)"

    expressions = read_all_expressions(source)
    assert len(expressions) == 1
    call_expr = expressions[0]
    # safety checks
    assert represent(call_expr).value == "(f 2)"

    # do the eval
    result = evaluate(global_environment, call_expr)

    assert result.type == int_type
    assert result.value == 5


# TODO: run the expressions in source/test/3-compute.lisp
def test_all_computes():
    from parse import source_map, tokenize, read_expr, parse_expr
    from native_builtins import global_environment, represent
    from interpreter import evaluate
    with open("source/test/3-compute.lisp") as f:
        source = f.read()
    chars = source_map(source)
    tokens = tokenize(chars)
    tokens.reverse()


    # (define f (lambda (x) x))
    expr = read_expr(tokens)
    assert represent(expr).value == "(define f (lambda (x) x))"

    result = evaluate(global_environment, expr)

    # print(represent(global_environment).value)

    code = "(f 4)"
    parsed = parse_expr(code)
    # assert represent(parsed).value == "(f 4)"
    result = evaluate(global_environment, parsed)

    from value.types import int_type
    assert result.type == int_type
    assert result.value == 4


    #print(represent(global_environment).value)

    # (define f (lambda (x) nil))
    expr = read_expr(tokens)
    assert represent(expr).value == "(define f (lambda (x) nil))"
    evaluate(global_environment, expr)


    # TODO: inspect the f function
    # inspect the closure environment
    # improve the environment debugging
    #   (print recursively)
    #   (print-environment)

    # TODO:
    # add a constructor for hashtables (environments)
    # add new functions for (set-exec-mode)

    # TODO: solve the compute scoping logic

    #code = parse_expr("(f 1)")
    #result = evaluate(global_environment, code)

    #print(represent(result).value)




    assert False

def test_compute_macro():
    pass

def test_compute_special():
    pass


def test_macroexpand():
    pass

