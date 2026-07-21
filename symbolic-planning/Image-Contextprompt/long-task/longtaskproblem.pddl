;; problem.pddl
;; Scene: mug nested in bowl, bowl inside a closed drawer, bottle on the
;; table. Goal: mug, bowl, and bottle all on the table, drawer closed,
;; and liquid poured from the bottle into the mug.

(define (problem table-setup-scene1)
  (:domain table-setup)

  (:objects
    drawer1              - drawer
    loc-drawer loc-table - location
    mug bowl bottle      - item
  )

  (:init
    ;; robot state
    (robot-at loc-drawer)
    (hand-empty)

    ;; static facts
    (loc-of drawer1 loc-drawer)
    (table-loc loc-table)

    ;; drawer state
    (closed drawer1)

    ;; object arrangement: mug nested in bowl, bowl inside the drawer
    (nested mug bowl)
    (inside bowl drawer1)

    ;; bottle starts on the table, already containing liquid
    (on-table bottle)
    (has-liquid bottle)
  )

  (:goal
    (and
      (on-table mug)
      (on-table bowl)
      (on-table bottle)
      (closed drawer1)
      (has-liquid mug)
    )
  )
)
