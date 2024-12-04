from value import hashtable, unique


def environment(parent=unique.nil):
    bindings = {
        "parent-scope": parent,
    }
    lisp_value = hashtable.hashtable(bindings)
    bindings["current-scope"] = lisp_value
    return lisp_value


global_environment = environment()

