(define (problem manipulation-task)
  (:domain manipulation)

  (:objects
    bottle cup bowl - object
    drawer - container
  )

  (:init
    (on-table bottle)
    (inside-drawer cup drawer)
    (inside-drawer bowl drawer)
    (on-top-of cup bowl)
    (closed drawer)
    (hand-empty)
  )

  (:goal
    (and
      (on-table cup)
      (on-table bowl)
      (poured)
      (closed drawer)
    )
  )
)
