"""
Debugging utilities

Implemented outside of builtins in order to import and use them from inside the interpreter
"""


from value.value import Value
from value.types import *
from value.unique import nil
from value.cell import car, cdr

from value.string import string


def to_string(x: Value):
    if x.type == int_type:
        return string(str(x.value))
    elif x.type == str_type:
        return x
    elif x.type == symbol_type:
        return string(x.value)
    elif x.type == cell_type:
        result = "("
        # while not nil
        while x != nil:
            head = car(x)
            x = cdr(x)
            result += represent(head).value
            if x != nil:
                result += " "
        result += ")"
        return string(result)
    else:
        raise Exception(f"to-string not implemented for type {x.type.value}")


def represent(x: Value):
    if x.type in (int_type, symbol_type, cell_type):
        return to_string(x)
    if x.type == str_type:
        return string(f'"{x.value}"')
    if x.type == hashtable_type:
        # {a: 'x} -> (dict\n :a 'x)
        h = {}
        for key, val in x.value.items():
            if key == "current-scope" and val is x:
                continue
            h[key] = represent(val).value

        lines = []
        for key, val in h.items():
            # generate (multiline) entry with dynamic indentation
            # here be dragons
            value_lines = val.split("\n")
            key_prefix = f"      :{key} "
            indent_prefix = " " * len(key_prefix)
            first_line, *value_lines = value_lines
            first_line = f"{key_prefix}{first_line}"
            entry_lines = [f"{indent_prefix}{line}" for line in value_lines]
            entry_lines.insert(0, first_line)
            lines.extend(entry_lines)
        result = "\n".join(lines)
        if result:
            return string(f"(dict\n{result})")
        else:
            return string("(dict)")
    if x.type == unique_type:
        return string(x.value)
    if x.type == function_type:
        assert x.value.type is cell_type
        exec_mode = car(x.value)
        func_val = cdr(x.value)
        func_val_repr = represent(func_val).value
        if exec_mode.value != "after-eval":
            return string(f"(function :{exec_mode.value} {func_val_repr})")
        else:
            return string(func_val_repr)
        #return string(f"<{exec_mode.value}> " + represent(func_val).value)
        #return string(result)
    if x.type == native_function_type:
        python_function = x.value
        return string(f"<native function {python_function.__name__}>")
    #if x.type == type_type:
    #    return 
    elif x.type == lisp_function_type:
        arglist = car(x.value)
        arglist_repr = represent(arglist).value
        body = car(cdr(x.value))
        body_repr = represent(body).value[1:-1]
        return string(f"(lambda {arglist_repr} {body_repr})")

    elif x.type == type_type:
        return string(f"<type {x.value}>")
    elif x.type == keyword_type:
        return string(f":{x.value}")
    else:
        raise Exception(f"repr not implemented for type {x.type.value}")

