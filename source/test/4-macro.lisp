(define no-eval (kw "no-eval"))

(define my-quote
  (function no-eval
            (lambda (x) x)))

(my-quote x)

(define my-macro
  (function (kw "before-eval")
            (lambda ()
              (print "macro expansion")
              (my-quote (print "generated code")))))

(my-macro)

(for (i (range 10))
        (my-macro)
        5)
