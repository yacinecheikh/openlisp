"""
recursive descent parser with incremental reader

uses a tokenizer
"""


class Token:
    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({repr(self.type)} {repr(self.value)})"

    # used in unit tests
    def __eq__(self, other):
        return self.type == other.type and self.value == other.value


# state machine
def next_token(source: str, i: int) -> (int, Token):
    buffer = []
    state = "default"
    while i < len(source):
        ch = source[i]
        if state == "default":
            if ch == "(":
                return i + 1, Token("syntax", "(")
            elif ch == ")":
                return i + 1, Token("syntax", ")")
            elif ch in (" ", "\n"):
                pass
            elif ch.isdigit():
                state = "number"
                buffer.append(ch)
            elif ch == '"':
                state = "string"
                buffer.append(ch)
            else:
                state = "symbol"
                buffer.append(ch)

        elif state == "number":
            if ch.isdigit():
                buffer.append(ch)
            elif ch in ("(", ")", " ", "\n"):
                number = "".join([ch for ch in buffer])
                token = Token("number", number)
                return i, token
            else:
                raise Exception(f"Invalid number at {repr(ch)}")

        elif state == "symbol":
            if ch in ("(", ")", " ", "\n"):
                # finish the symbol parsing
                symbol = "".join([ch for ch in buffer])
                token = Token("symbol", symbol)
                return i, token
            else:
                buffer.append(ch)

        elif state == "string":
            if ch == '"':
                buffer.append(ch)
                # remove the quotes
                buffer = buffer[1:-1]
                string = "".join([ch for ch in buffer])
                token = Token("string", string)
                return i + 1, token
            else:
                buffer.append(ch)

        i += 1
    # no token left
    if state == "default":
        assert i == len(source)
        return i, None
    # EOF: finish reading current token
    if state == "number":
        return i, Token("number", "".join(buffer))
    if state == "symbol":
        return i, Token("symbol", "".join(buffer))
    if state == "string":
        raise ValueError("Incomplete string literal")
    raise NotImplementedError


from value.value import Value  # typing
from value.symbol import symbol
from value.integer import integer
from value.string import string
from value.unique import nil
from value.cell import cons, car, cdr, reverse


# recursive descent reader
def next_expr(source: str, i: int) -> (int, Value):
    next_i, token = next_token(source, i)
    # no expression left
    if token is None:
        return i, None
    i = next_i

    if token.type == "symbol":
        s = symbol(token.value)
        return i, s
    elif token.type == "number":
        n = integer(int(token.value))
        return i, n
    elif token.type == "string":
        s = string(token.value)
        return i, s
    elif token.type == "syntax" and token.value == "(":
        sub_exprs = nil
        while True:
            next_i, token = next_token(source, i)
            if token is None:
                raise Exception(f"Unexpected end of file while parsing s-expression")
            elif token.type == "syntax" and token.value == ")":
                # break condition
                result = reverse(sub_exprs)
                return next_i, result
            else:
                i, expr = next_expr(source, i)
                sub_exprs = cons(expr, sub_exprs)
    else:
        raise Exception("Unknown token type")


# wrapper for sequential evaluation during tests
def read_all_expressions(source):
    expressions = []
    i = 0
    while True:
        i, expr = next_expr(source, i)
        if expr is None:
            break
        expressions.append(expr)
    return expressions

