# Roadmap

Base Interpreter:
- [x] runtime
- [x] parser
- [x] inspection and printing utilities
- [x] interpreter
- [x] builtins
- [x] test coverage

Fixes before bootstrapping:
- [ ] The for loop does not create a new scope to define the iteration variable
- [ ] implement missing builtins
- [ ] implement unnamed symbols for (gensym)
- [ ] cleanup calls to `(compute)` in unit tests and finish removing parameter evaluation from `(compute)`

Bootstrapping:
- [ ] generate the base interpreter by running an Openlisp program
- [ ] develop code generation utilities
- [ ] replace the base interpreter with Openlisp code
