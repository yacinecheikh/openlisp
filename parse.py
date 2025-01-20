# recursive descent (tokenizer)
# tokenizer
# map every step of the compilation

# source mapping
class Char:
    def __init__(self, ch: str, line: int, position: int):
        self.ch = ch
        self.line = line
        self.position = position
    def __repr__(self):
        return f"Ch({repr(self.ch)} ({self.line}:{self.position}))"

def source_map(source: str):
    line = 1
    position = 1
    result = []
    for ch in source:
        result.append(Char(ch, line, position))
        position += 1
        if ch == "\n":
            position = 1
            line += 1
    return result

#with open("source/source_map.lisp", "r") as f:
#    print(source_map(f.read()))

from typing import List

class Token:
    def __init__(self, type: str, value: str, start_line, start_position, end_line, end_position):
        self.type = type
        self.value = value
        self.start_line = start_line
        self.start_position = start_position
        self.end_line = end_line
        self.end_position = end_position

    def __repr__(self):
        return f"Token({repr(self.type)} {repr(self.value)}) at {self.start_line}:{self.start_position}-{self.end_line}:{self.end_position}"


def tokenize(source: List[Char]) -> List[Token]:
    tokens = []
    buffer = []
    state = "default"
    i = 0
    while i < len(source):
        ch = source[i]
        if state == "default":
            if ch.ch == "(":
                tokens.append(Token("syntax", "(", ch.line, ch.position, ch.line, ch.position))
            elif ch.ch == ")":
                tokens.append(Token("syntax", ")", ch.line, ch.position, ch.line, ch.position))
            elif ch.ch in (" ", "\n"):
                pass
            elif ch.ch.isdigit():
                state = "number"
                buffer.append(ch)
            elif ch.ch == '"':
                state = "string"
                buffer.append(ch)
            else:
                state = "symbol"
                buffer.append(ch)
        elif state == "number":
            if ch.ch.isdigit():
                buffer.append(ch)
            elif ch.ch in ("(", ")", " ", "\n"):
                start_line, start_position = buffer[0].line, buffer[0].position
                end_line, end_position = buffer[-1].line, buffer[-1].position
                number = "".join([ch.ch for ch in buffer])
                token = Token("number", number, start_line, start_position, end_line, end_position)
                tokens.append(token)
                buffer = []
                i -= 1
                state = "default"
            else:
                raise Exception(f"Invalid number at {repr(ch)}")

        elif state == "symbol":
            if ch.ch in ("(", ")", " ", "\n"):
                # finish the symbol parsing
                start_line, start_position = buffer[0].line, buffer[0].position
                end_line, end_position = buffer[-1].line, buffer[-1].position
                symbol = "".join([ch.ch for ch in buffer])
                token = Token("symbol", symbol, start_line, start_position, end_line, end_position)
                tokens.append(token)
                buffer = []

                i -= 1
                state = "default"
            else:
                buffer.append(ch)

        elif state == "string":
            if ch.ch == '"':
                buffer.append(ch)
                start_line, start_position = buffer[0].line, buffer[0].position
                end_line, end_position = buffer[-1].line, buffer[-1].position
                # remove the quotes
                buffer = buffer[1:-1]
                string = "".join([ch.ch for ch in buffer])
                token = Token("string", string, start_line, start_position, end_line, end_position)
                tokens.append(token)
                buffer = []
                state = "default"
            else:
                buffer.append(ch)

        i += 1
    return tokens


#with open("source/source_map.lisp", "r") as f:
#    source = f.read()
#    tokens = tokenize(source_map(source))
#    print(tokens)

from value.symbol import symbol
from value.integer import integer
from value.string import string
from value.unique import nil
from value.cell import cons, car, cdr, reverse

# recursive descent
def read_expr(tokens: List[Token]):
    if not tokens:
        return None

    token = tokens.pop()

    if token.type == "symbol":
        s = symbol(token.value)
        s.start_position = token.start_position
        s.start_line = token.start_line
        s.end_position = token.end_position
        s.end_line = token.end_line
        return s
    elif token.type == "number":
        n = integer(int(token.value))
        n.start_position = token.start_position
        n.start_line = token.start_line
        n.end_position = token.end_position
        n.end_line = token.end_line
        return n
    elif token.type == "string":
        s = string(token.value)
        s.start_position = token.start_position
        s.start_line = token.start_line
        s.end_position = token.end_position
        s.end_line = token.end_line
        return s
    elif token.type == "syntax" and token.value == "(":
        start_position = token.start_position
        start_line = token.start_line
        sub_exprs = nil
        while True:
            if len(tokens) == 0:
                raise Exception(f"Unexpected end of file while parsing s-expression at {start_line}:{start_position}")
            token = tokens[-1]
            if token.type == "syntax" and token.value == ")":
                end_position = token.end_position
                end_line = token.end_line
                # end of list
                tokens.pop()
                result = reverse(sub_exprs)
                result.start_position = start_position
                result.start_line = start_line
                result.end_position = end_position
                result.end_line = end_line
                return result
            else:
                expr = read_expr(tokens)
                sub_exprs = cons(expr, sub_exprs)
    else:
        raise Exception("Unknown token type")

# tokenizer
#def tokenize(source: str) -> list:
    # (eq x y)
    # "(", "eq", "x", "y", ")"



def parse_expr(source):
    chars = source_map(source)
    tokens = tokenize(chars)
    tokens.reverse()

    expr = read_expr(tokens)
    assert not tokens
    return expr

