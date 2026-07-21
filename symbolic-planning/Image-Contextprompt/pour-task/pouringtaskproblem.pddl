(define (problem pour-bottle-into-cup)
  (:domain pouring-manipulation)

  (:objects
    robot1 - robot
    bottle cup - item
    loc-bottle loc-cup - location
  )

  (:init
    (robot-at robot1 loc-bottle)
    (obj-at bottle loc-bottle)
    (obj-at cup loc-cup)
    (gripper-empty robot1)
    (has-liquid bottle)
  )

  (:goal (and
    (has-liquid cup)
    (obj-at bottle loc-bottle)
    (gripper-empty robot1)
  ))
)
