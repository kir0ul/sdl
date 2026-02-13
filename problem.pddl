(define (problem kitchen_task_1)
  (:domain kitchen_robot)
  (:objects bottle bowl cup - physobj)

  (:init
    (hand-empty)
    (drawer-closed)
    (on-table bottle)
    (clear bottle)
    
    (inside-drawer bowl)
    (inside-drawer cup)
    (on cup bowl)   ;; Cup is on the bowl
    (clear cup)     ;; Bowl is NOT clear
  )

  (:goal (and
    (on-table cup)
    (on-table bowl)
    (poured bottle cup)
    (drawer-closed)
  ))
)
