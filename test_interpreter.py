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


# TODO: define "define"
def test_compute_lisp():
    from parse import source_map, tokenize, read_expr
    from native_builtins import represent
    with open("source/test/2-define.lisp") as f:
        source = f.read()
    chars = source_map(source)
    tokens = tokenize(chars)

    # read and evaluate one expression at a time
    tokens.reverse()
    simple_define_expr = read_expr(tokens)
    lambda_define_expr = read_expr(tokens)
    assert not tokens
    assert represent(simple_define_expr).value == "(define x 5)"
    assert represent(lambda_define_expr).value == "(define f (lambda (x) nil))"

    from native_builtins import global_environment
    from interpreter import evaluate
    result = evaluate(global_environment, simple_define_expr)

    print(represent(global_environment).value)

    # TODO

    assert False


def test_compute_macro():
    pass

def test_compute_special():
    pass


def test_eval_funcall():
    pass


def test_macroexpand():
    pass

