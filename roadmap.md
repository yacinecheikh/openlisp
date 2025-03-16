# Roadmap

Interpreter implementation:
- [x] runtime
- [x] parser
- [x] inspection and printing utilities
- [x] interpreter
- [x] builtins
- [x] test coverage

Bugs fixes:
- [ ] The for loop does not create a new scope to define the iteration variable

Missing features:
- [ ] implement missing builtins
- [ ] implement unnamed symbols for (gensym)

Cleanup:
- [ ] Rewrite calls to `(compute)` in unit tests and finish removing evaluation from `(compute)`
