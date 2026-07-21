(define (domain pour-liquid-domain)

  (:requirements :typing :negative-preconditions)

  (:types
    location
    object
    container - object
  )

  (:predicates
    (robot-at ?loc - location)
    (object-at ?obj - object ?loc - location)
    (holding ?obj - object)
    (gripper-empty)
    (has-liquid ?c - container)
    (tilted ?obj - object)
  )

  ;; ---------------------------------------------------------
  ;; Move the robot symbolically between two locations
  ;; ---------------------------------------------------------
  (:action move
    :parameters (?from - location ?to - location)
    :precondition (and
      (robot-at ?from)
    )
    :effect (and
      (not (robot-at ?from))
      (robot-at ?to)
    )
  )

  ;; ---------------------------------------------------------
  ;; Grasp an object that is at the robot's current location
  ;; ---------------------------------------------------------
  (:action grasp
    :parameters (?obj - object ?loc - location)
    :precondition (and
      (robot-at ?loc)
      (object-at ?obj ?loc)
      (gripper-empty)
    )
    :effect (and
      (holding ?obj)
      (not (gripper-empty))
      (not (object-at ?obj ?loc))
    )
  )

  ;; ---------------------------------------------------------
  ;; Tilt a held object in preparation for pouring
  ;; ---------------------------------------------------------
  (:action tilt
    :parameters (?obj - object)
    :precondition (and
      (holding ?obj)
      (not (tilted ?obj))
    )
    :effect (and
      (tilted ?obj)
    )
  )

  ;; ---------------------------------------------------------
  ;; Pour liquid from a held, tilted container into a
  ;; target container located at the robot's current location
  ;; ---------------------------------------------------------
  (:action pour
    :parameters (?source - container ?target - container ?loc - location)
    :precondition (and
      (holding ?source)
      (tilted ?source)
      (robot-at ?loc)
      (object-at ?target ?loc)
      (has-liquid ?source)
      (not (has-liquid ?target))
    )
    :effect (and
      (not (has-liquid ?source))
      (has-liquid ?target)
    )
  )

  ;; ---------------------------------------------------------
  ;; Rotate a held object back to an upright orientation
  ;; ---------------------------------------------------------
  (:action rotate
    :parameters (?obj - object)
    :precondition (and
      (holding ?obj)
      (tilted ?obj)
    )
    :effect (and
      (not (tilted ?obj))
    )
  )

  ;; ---------------------------------------------------------
  ;; Place a held, upright object down at the current location
  ;; ---------------------------------------------------------
  (:action place
    :parameters (?obj - object ?loc - location)
    :precondition (and
      (holding ?obj)
      (robot-at ?loc)
      (not (tilted ?obj))
    )
    :effect (and
      (object-at ?obj ?loc)
      (gripper-empty)
      (not (holding ?obj))
    )
  )

)