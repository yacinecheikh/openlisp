# Openlisp

A Lisp designed to cross-compile to everything

## Goals

Openlisp is an interpreted Lisp inspired by Haxe.

The core idea behind Openlisp is to generate code for other languages and platforms from a cross-compiled interpreter.

Here are some examples of what Openlisp tries to do:
- generate, compile and execute low level code directly from the Lisp interpreted runtime
- run in a browser by cross-compiling the interpreter to Javascript
- use libraries and features from other languages
- produce and run programs on the fly in different languages
- having the complete code generation, compiler and build pipeline available during runtime

Technically, Openlisp is not a cross-compiled language.
Openlisp is an interpreted language with foreign code generation capabilities, which is used to generate its own interpreter. This distinction is important because the focus of Openlisp is not being performant nor being a proper useable language.


During development, I also tried to maintain a clean codebase for what would be an easy to understand and extend Lisp interpreter.
If you are interested in the implementation of a Lisp, please read [the architecture documentation](./architecture.md).



## Status

The current progress can be checked in [the roadmap](./roadmap.md). The base (Python) interpreter is complete, but has not been bootstrapped yet.

