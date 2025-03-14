# Architecture

## Interpreter

As of v0.1, the (Python) interpreter is based on a stack of layers:
- Runtime
- Printing utilities
- Reader
- Interpreter
- Builtins

Each of these layers is covered by unit tests, because the behavior of an interpreter is much harder to debug as it grows in complexity.

The total source code is only 896 LoC:
- `value/*.py` (runtime): 223 LoC
- `parse.py` (reader): 142 LoC
- `utils.py` (pretty print, used for debugging): 107 LoC
- `interpreter.py` (the full interpreter): 212 LoC
- `native_builtins.py` (the lisp builtins): 212 LoC



### Runtime

Relevant files: `value/`

The Lisp runtime is exclusively composed of Lisp values.
Lexical scoping is implented using Lisp hashtables.
Functions defined in are implemented as a closure scope, a symbol list for parameters and a list of s-expressions for its body.

Lisp values are also used to represent Lisp code itself. Variables are represented as symbols, function calls are represented as Lisp lists,...

This allows the Lisp runtime to be entirely programmable from Lisp itself, including the Lisp reader.

Lisp values are implemented as a pair of a type and a Python-encoded value.

The type of a Lisp value is itself also a Value at runtime (with the type of types being its own type).
This type system is taken from Python, where every value is an instance of a class, and `type` is the metaclass of all types.

The encoding of a Lisp value depends on its type. For example, Lisp strings and integers are simply encoded as Python strings and integers. Symbols and keywords are both represented by Python strings. More complex datatypes, like Lisp functions, are encoded as other Lisp values, like linked lists.

The exact encoding of Lisp types is not important, since the Openlisp interpreter is intended to be cross-compiled to many different languages, with different implementations depending on the target languages.


One peculiarity of Openlisp is a dedicated `unique`datatype for unique and distinct values, like `nil`, `true` and `false`.
This datatype makes it possible in the future to define enums as a set of unique distinct values or create placeholders constants for types that require a base value like linked lists or binary trees.
The Python implementation is as simple as creating a Value instance, since Python object equality is defined by identity (or memory address equality).


### Printing utilities

Relevant files: `utils.py`, `test_utils.py`

In order to easily debug the interpreter and future Openlisp programs, value printing functions are essential.

Openlisp uses 2 functions to represent values: `(repr)` and `(to-string)`.

These functions are equivalent to Python's `repr()` and `str()` functions: `str` simply converts to a string, and `repr` creates a Python representation of the value.
For example, converting `"text"` to a string in Python using `str` would simply return the string itself, and printing it would print the characters `text`.
However, using `repr` will convert the string to a Python string literal: `"'test'"`, and printing it would display `'text'`.

The `(repr)` function in lisp is critical for inspecting Lisp values, as it makes the type of the value explicit through its representation.

Since everything is a Lisp value, the `(repr)` function can also be used to display the definition of a function as understood by the interpreter, or display the contents of a variable environment at any given time.


### Reader

Relevant files: `parse.py`, `test_parser.py`

The lisp reader is traditionally an incremental recursive descent value parser.

Being an incremental parser means that a Lisp compile can read, compile and execute code step by step instead of looking ahead of the current instruction.
This allows the language to edit the state of the compiler and extend the language directly from the code, by executing Lisp code before reading and compiling the rest of the program.

Being a value parser means that the reader returns Lisp values to represent code. These values can in turn be manipulated by the Lisp program before its execution.

A recursive descent parser is just a parser written as a set of recursive functions to parse the recursive syntax of a language.

The parser of Openlisp also uses a tokenizer (a state machine) to simplify the parser.


### Interpreter
Relevant files: `interpreter.py`, `test_interpreter.py`

The Openlisp interpreter is similar to most other Lisps. It features:
- a global symbol table
- lexical scoping
- expanding macros ahead of execution

Reader macros are not supported yet.
Instead of implementing a reader macro API, the plan is to allow overriding the builtin (read) function with a Lisp-defined function.
This would allow much more flexibility for the user of Openlisp as the Openlisp code can be inspected and modified by the user.


Another unique feature of Openlisp is special functions. Special functions are mostly used to implement builtins, but they can also be used to bootstrap features with custom evaluation rules like `(quote)` or `(and)`.

In Openlisp, every function is flagged with an execution mode, which determines if a function is a function (evaluated after its arguments), a macro (evaluated before its result) or a special function (neither arguments nor results are evaluated).

The last execution mode, `:no-eval`, can be used to define runtime functions which can manually choose to evaluate their parameters. This flag is used to implement all the core builtins: `(if)`, `(define)`, `(quote)`,...
This allows keeping builtins and macros as first class values at runtime, and makes the interpreter more modular.

An interesting side effect is that bootstrapping`(quote)` becomes trivial:
```
(define my-quote
        (function (kw "no-eval")
                  (lambda (x) x)))
```


### Builtins

Relevant files: `native_builtins.py`, `test_interpreter.py`

Openlisp builtins are usually defined as wrapped Python functions.

Here is the list of currently defined builtins:
- `true`
- `false`
- `nil`
- `(to-string)`
- `(repr)`
- `(print)`
- `(quote)`
- `(define)`
- `(lambda)`
- `(for)`
- `(range)`
- `(kw)`
- `(function)`


#### For loop

The `(for)` loop is a for each loop, and expects an iterator. Iterators are functions (usually closures) which are called until they stop producing values.
For example, `(range 5)` would return a function that will return the following values when called in a loop:
```
(0) (1) (2) (3) (4) nil
```
As you can see in this example, each value is wrapped in a cons cell (a 1-element list), and the function returns nil when there is no value left.

This implementation of iterators is loosely inspired by Lua because of its simplicity.


#### Keywords

The `(kw)` builtin is a constructor for keywords:
```
(print (repr (kw "before-eval")))
-> :before-eval
```
There is currently no builtin syntax for keywords, although `(repr)` represents them with a prefix `:`. This is done in order to minimize the complexity of the parser until a more scalable alternative to the tokenizer state machine is found.


#### Function constructor

The `function` builtin is used to create functions with custom execution flags. It takes a function as a parameter, so it can only be used to add a different execution flag to the new function.

The supported execution flags are:
- `:after-eval`: used for functions (evaluate after arguments)
- `:before-eval`: used for macros (evaluate before the returned value)
- `:no-eval`: used for builtins (never evaluate arguments or returned values)


#### Missing builtins

Some builtins are planned but have not been implemented yet:
- `(quasiquote)`
- `(gensym)`
- `(if)`
- `(and)`, `(or)`, `(<)`, `(<=)`, `(>)`, `(>=)`, `(==)`
- `(set)`

