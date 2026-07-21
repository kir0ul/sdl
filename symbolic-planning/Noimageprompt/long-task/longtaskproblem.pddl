(define (problem drawer-tableware-scene)
  (:domain drawer-tableware-manipulation)

  (:objects
    mug bowl bottle - item
    drawer - container
    loc-drawer loc-mug-pos loc-bowl-pos loc-bottle-orig - location
  )

  (:init
    ;; container setup
    (container-at drawer loc-drawer)
    (closed drawer)

    ;; storage nesting: bowl in drawer, mug on top of bowl
    (in-container bowl drawer)
    (on-top mug bowl)
    (clear mug)

    ;; bottle standing on table
    (at bottle loc-bottle-orig)
    (clear bottle)
    (has-liquid bottle)

    ;; robot / gripper state
    (robot-at loc-bottle-orig)
    (hand-empty)
  )

  (:goal
    (and
      (at mug loc-mug-pos)
      (at bowl loc-bowl-pos)
      (closed drawer)
      (has-liquid mug)
      (at bottle loc-bottle-orig)
      (hand-empty)
    )
  )
)