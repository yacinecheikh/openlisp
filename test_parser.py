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
    assert tokens[5] == Token("syntax", "(")
    assert tokens[6] == Token("number", "1")
    assert tokens[7] == Token("number", "2")
    assert tokens[8] == Token("number", "3")
    assert tokens[9] == Token("syntax", ")")
    assert tokens[10] == Token("symbol", "f")
    assert len(tokens) == 11



def test_read():
    from native_builtins import to_string, represent#, inspect
    from parse import read_all_expressions
    exprs = read_all_expressions(open("source/test/1-read.lisp").read())
    assert len(exprs) == 6
    assert represent(exprs[0]).value == "nil"
    assert represent(exprs[1]).value == "52334"
    assert represent(exprs[2]).value == "\"test\""
    assert represent(exprs[3]).value == "var"
    assert represent(exprs[4]).value == "(1 2 3)"
    assert represent(exprs[5]).value == "f"

