(define (problem serve-mug-and-bowl)
  (:domain robotic-object-serving)

  (:objects
    mug bowl - object
    table-loc mug-serving-loc bowl-serving-loc - location
  )

  (:init
    (robot-at table-loc)
    (gripper-empty)
    (at bowl table-loc)
    (in mug bowl)
  )

  (:goal
    (and
      (at mug mug-serving-loc)
      (at bowl bowl-serving-loc)
      (gripper-empty)
    )
  )
)