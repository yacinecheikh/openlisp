def read_all_tokens(path):
    from parse import next_token
    with open(path) as f:
        source = f.read()
        i = 0
        while True:
            i, token = next_token(source, i)
            if token is None:
                break
            yield token

def test_tokenizer():
    from native_builtins import to_string, represent #, inspect
    from parse import Token
    tokens = list(read_all_tokens("source/test/1-read.lisp"))
    """
    source code:
    ()
    52334
    "test"
    var
    """
    assert tokens[0] == Token("syntax", "(")
    assert tokens[1] == Token("syntax", ")")
    assert tokens[2] == Token("number", "52334")
    assert tokens[3] == Token("string", "test")
    assert tokens[4] == Token("symbol", "var")
    assert len(tokens) == 5



def read_all_expressions(path):
    from parse import next_expr
    with open(path) as f:
        source = f.read()
        i = 0
        while True:
            i, expr = next_expr(source, i)
            if expr is None:
                break
            yield expr

def test_read():
    from native_builtins import to_string, represent#, inspect
    exprs = list(read_all_expressions("source/test/1-read.lisp"))
    assert len(exprs) == 4
    assert represent(exprs[0]).value == "nil"
    assert represent(exprs[1]).value == "52334"
    assert represent(exprs[2]).value == "\"test\""
    assert represent(exprs[3]).value == "var"

