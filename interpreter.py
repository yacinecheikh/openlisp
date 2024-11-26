env = { "a": 5 }
{ "parent-scope": env }


def lookup(env, symbol):
    pass

def compute(env, func, args):
    """
    (f a b c)
    f = cons(arglist, body, func_env)
    local_env = {(func_env)}
    for arg in args:
        local_env[arglist[0]] = a

    for expr in body:
    """
    pass


def expand(env, expr):
    """
    (defmacro g ...)
    (f (g (h 5)))
    """
    pass


def evaluate(env, expr):
    """
    5 "test" -> return
    x -> lookup
    (a b (c)) -> expand; (evaluate parameters?); compute; (evaluate the result?)
    """
    pass





##### lexical binding example
"""
(defun g ()
        (let ((counter 0))
          (lambda (x)
            (setf counter (+ counter x))
             counter)))


(defvar increment-counter (g))
(increment-counter 5)
"""


