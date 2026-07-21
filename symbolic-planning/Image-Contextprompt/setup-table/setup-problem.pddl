;; problem.pddl
;; Scene: mug nested inside bowl, both in an open wire basket ("drawer") on the table.
;; Goal: mug placed at its designated table spot, bowl placed beside it,
;;       gripper ends empty.

(define (problem table-setting-mug-bowl)
  (:domain table-setting)

  (:objects
    mug bowl - item
    drawer_loc mug_target_loc bowl_target_loc - location
  )

  (:init
    (robot-at drawer_loc)
    (item-at bowl drawer_loc)
    (inside mug bowl)
    (gripper-empty)
  )

  (:goal
    (and
      (item-at mug mug_target_loc)
      (item-at bowl bowl_target_loc)
      (gripper-empty)
    )
  )
)
