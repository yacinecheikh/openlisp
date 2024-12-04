def test_tokenizer():
    from native_builtins import to_string, represent, inspect
    from parse import source_map, tokenize, read_expr
    with open("source/test/1-read.lisp") as f:
        chars = source_map(f.read())
        tokens = tokenize(chars)
        print(tokens)
        assert len(tokens) == 8
        assert tokens[0].type == "number"
        assert tokens[1].type == "number"
        assert tokens[2].type == "string"
        assert tokens[3].type == "symbol"
        assert tokens[4].type == "syntax"
        assert tokens[5].type == "symbol"
        assert tokens[6].type == "string"
        assert tokens[7].type == "syntax"

        assert tokens[0].value == "6403840"
        assert tokens[1].value == "112"
        assert tokens[2].value == "sirte"
        assert tokens[3].value == "variable"
        assert tokens[4].value == "("
        assert tokens[5].value == "print"
        assert tokens[6].value == "hello world"
        assert tokens[7].value == ")"

        #tokens.reverse()
        #while tokens:
        #    expr = read_expr(tokens)
        #    print(inspect(expr).value)


def test_source_mapped_tokens():
    #Token('number' '6403840') at 3:1-3:7, Token('number' '112') at 5:1-5:3, Token('string' 'sirte') at 7:1-7:7, Token('symbol' 'variable') at 9:1-9:8, Token('syntax' '(') at 11:1-11:1, Token('symbol' 'print') at 11:2-11:6, Token('string' 'hello world') at 11:8-11:20, Token('syntax' ')') at 11:21-11:21]
    from native_builtins import to_string, represent, inspect
    from parse import source_map, tokenize, read_expr
    with open("source/test/1-read.lisp") as f:
        chars = source_map(f.read())
        tokens = tokenize(chars)
        print(tokens)


    assert False


def test_parse():
    from native_builtins import to_string, represent, inspect
    from parse import source_map, tokenize, read_expr
    with open("source/test/1-read.lisp") as f:
        chars = source_map(f.read())
        tokens = tokenize(chars)
        print(tokens)

        #tokens.reverse()
        #while tokens:
        #    expr = read_expr(tokens)
        #    print(inspect(expr).value)

    assert False


