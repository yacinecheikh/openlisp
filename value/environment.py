from value import hashtable, unique, string
from value.types import hashtable_type, symbol_type
from value.value import Value


def environment(parent=unique.nil):
    bindings = {
        "parent-scope": parent,
    }
    lisp_value = hashtable.hashtable(bindings)
    bindings["current-scope"] = lisp_value
    return lisp_value

# wrapper over hashtable.setkey
# uses symbols instead of strings as keys
def bind(env: Value, symb: Value, value: Value):
    assert env.type == hashtable_type
    assert symb.type == symbol_type
    hashtable.setkey(env, string.string(symb.value), value)


global_environment = environment()

