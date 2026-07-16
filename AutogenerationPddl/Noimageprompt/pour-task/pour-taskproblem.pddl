(define (problem pour-bottle-into-mug)
  (:domain pour-liquid-domain)

  (:objects
    bottle mug   - container
    start_loc bottle_loc mug_loc - location
  )

  (:init
    (robot-at start_loc)
    (object-at bottle bottle_loc)
    (object-at mug mug_loc)
    (gripper-empty)
    (has-liquid bottle)
    ;; mug has no liquid (absence of has-liquid mug)
    ;; bottle is not tilted (absence of tilted bottle)
  )

  (:goal
    (and
      (object-at bottle bottle_loc)
      (has-liquid mug)
      (gripper-empty)
      (not (has-liquid bottle))
    )
  )
)