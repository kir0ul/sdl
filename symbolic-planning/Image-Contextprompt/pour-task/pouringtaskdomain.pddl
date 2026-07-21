(define (domain pouring-manipulation)
  (:requirements :strips :typing)

  (:types
    robot item location
  )

  (:predicates
    (robot-at ?r - robot ?l - location)      ; robot's current symbolic location
    (obj-at ?i - item ?l - location)         ; item's current symbolic location (only when not held)
    (holding ?r - robot ?i - item)           ; robot is currently holding item ?i
    (gripper-empty ?r - robot)               ; robot's gripper is free
    (has-liquid ?i - item)                   ; item currently contains/holds liquid
  )

  ;; ---------------------------------------------------------
  ;; move: robot travels between two symbolic locations
  ;; ---------------------------------------------------------
  (:action move
    :parameters (?r - robot ?from - location ?to - location)
    :precondition (and
      (robot-at ?r ?from)
    )
    :effect (and
      (not (robot-at ?r ?from))
      (robot-at ?r ?to)
    )
  )

  ;; ---------------------------------------------------------
  ;; grasp: robot picks up an item at its current location
  ;; ---------------------------------------------------------
  (:action grasp
    :parameters (?r - robot ?i - item ?l - location)
    :precondition (and
      (robot-at ?r ?l)
      (obj-at ?i ?l)
      (gripper-empty ?r)
    )
    :effect (and
      (holding ?r ?i)
      (not (obj-at ?i ?l))
      (not (gripper-empty ?r))
    )
  )

  ;; ---------------------------------------------------------
  ;; pour: robot, holding a filled item, pours its liquid
  ;;       into another item co-located with the robot
  ;; ---------------------------------------------------------
  (:action pour
    :parameters (?r - robot ?src - item ?dst - item ?l - location)
    :precondition (and
      (robot-at ?r ?l)
      (holding ?r ?src)
      (obj-at ?dst ?l)
      (has-liquid ?src)
    )
    :effect (and
      (has-liquid ?dst)
    )
  )

  ;; ---------------------------------------------------------
  ;; place: robot places the held item down at its current
  ;;        location and releases it (gripper becomes free)
  ;; ---------------------------------------------------------
  (:action place
    :parameters (?r - robot ?i - item ?l - location)
    :precondition (and
      (robot-at ?r ?l)
      (holding ?r ?i)
    )
    :effect (and
      (obj-at ?i ?l)
      (not (holding ?r ?i))
      (gripper-empty ?r)
    )
  )
)
