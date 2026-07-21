;; domain.pddl
;; Domain: Tabletop manipulation - unstacking a nested item and setting it on a table
;; Reusable for any task where a small item is nested inside a container item,
;; and both must end up placed at designated table locations, item-first then container.

(define (domain table-setting)

  (:requirements :strips :typing)

  (:types
    item      ; movable objects, e.g. mug, bowl
    location  ; symbolic places: drawer/basket location, table target locations
  )

  (:predicates
    (robot-at ?l - location)          ; robot's current symbolic location
    (item-at ?i - item ?l - location) ; item is resting at a free-standing location
    (inside ?i - item ?c - item)      ; item ?i is nested inside container item ?c
    (holding ?i - item)               ; gripper is currently holding item ?i
    (gripper-empty)                   ; gripper holds nothing
  )

  ;; ---------------------------------------------------------------
  ;; Move the robot base/arm symbolically between locations
  ;; ---------------------------------------------------------------
  (:action move
    :parameters (?from - location ?to - location)
    :precondition (and (robot-at ?from))
    :effect (and (not (robot-at ?from))
                 (robot-at ?to))
  )

  ;; ---------------------------------------------------------------
  ;; Remove an item that is nested inside a container item.
  ;; Represents extraction (e.g., lifting the mug out of the bowl).
  ;; ---------------------------------------------------------------
  (:action remove
    :parameters (?i - item ?c - item ?l - location)
    :precondition (and (robot-at ?l)
                        (inside ?i ?c)
                        (item-at ?c ?l)
                        (gripper-empty))
    :effect (and (holding ?i)
                 (not (inside ?i ?c))
                 (not (gripper-empty)))
  )

  ;; ---------------------------------------------------------------
  ;; Grasp an item that is free-standing (not nested) at a location.
  ;; ---------------------------------------------------------------
  (:action grasp
    :parameters (?i - item ?l - location)
    :precondition (and (robot-at ?l)
                        (item-at ?i ?l)
                        (gripper-empty))
    :effect (and (holding ?i)
                 (not (item-at ?i ?l))
                 (not (gripper-empty)))
  )

  ;; ---------------------------------------------------------------
  ;; Place a held item down at the robot's current location and
  ;; open the gripper (release is folded into place's effects).
  ;; ---------------------------------------------------------------
  (:action place
    :parameters (?i - item ?l - location)
    :precondition (and (robot-at ?l)
                        (holding ?i))
    :effect (and (item-at ?i ?l)
                 (not (holding ?i))
                 (gripper-empty))
  )

)
