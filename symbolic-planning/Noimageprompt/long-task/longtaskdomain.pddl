(define (domain drawer-tableware-manipulation)
  (:requirements :strips :typing)

  (:types
    item        ; movable objects: mug, bowl, bottle, etc.
    container   ; openable storage receptacles: drawer, cabinet, etc.
    location    ; symbolic workspace locations
  )

  (:predicates
    (robot-at ?l - location)                 ; robot's current symbolic location
    (container-at ?c - container ?l - location) ; container's fixed location
    (open ?c - container)                    ; container is open
    (closed ?c - container)                  ; container is closed
    (in-container ?i - item ?c - container)  ; item stored inside a container
    (on-top ?i1 - item ?i2 - item)           ; i1 rests on top of i2
    (at ?i - item ?l - location)             ; free-standing item's location
    (clear ?i - item)                        ; nothing rests on top of item i
    (holding ?i - item)                      ; gripper currently holds i
    (hand-empty)                             ; gripper holds nothing
    (has-liquid ?i - item)                   ; item currently contains liquid
  )

  ;; ---------- Locomotion ----------
  (:action move
    :parameters (?from - location ?to - location)
    :precondition (robot-at ?from)
    :effect (and (not (robot-at ?from)) (robot-at ?to))
  )

  ;; ---------- Container operations ----------
  (:action open
    :parameters (?c - container ?l - location)
    :precondition (and (robot-at ?l) (container-at ?c ?l)
                        (closed ?c) (hand-empty))
    :effect (and (open ?c) (not (closed ?c)))
  )

  (:action close
    :parameters (?c - container ?l - location)
    :precondition (and (robot-at ?l) (container-at ?c ?l)
                        (open ?c) (hand-empty))
    :effect (and (closed ?c) (not (open ?c)))
  )

  ;; ---------- Grasping ----------
  ;; Grasp an item that is stacked on top of another item inside an open container
  (:action grasp-stacked
    :parameters (?i1 - item ?i2 - item ?c - container ?l - location)
    :precondition (and (robot-at ?l) (container-at ?c ?l) (open ?c)
                        (in-container ?i2 ?c) (on-top ?i1 ?i2)
                        (clear ?i1) (hand-empty))
    :effect (and (holding ?i1) (not (hand-empty))
                 (not (on-top ?i1 ?i2)) (clear ?i2))
  )

  ;; Grasp an item resting directly inside an open container
  (:action grasp-from-container
    :parameters (?i - item ?c - container ?l - location)
    :precondition (and (robot-at ?l) (container-at ?c ?l) (open ?c)
                        (in-container ?i ?c) (clear ?i) (hand-empty))
    :effect (and (holding ?i) (not (hand-empty))
                 (not (in-container ?i ?c)))
  )

  ;; Grasp an item resting freely on a surface/location
  (:action grasp-from-surface
    :parameters (?i - item ?l - location)
    :precondition (and (robot-at ?l) (at ?i ?l) (clear ?i) (hand-empty))
    :effect (and (holding ?i) (not (hand-empty)) (not (at ?i ?l)))
  )

  ;; ---------- Placing / Releasing ----------
  (:action place
    :parameters (?i - item ?l - location)
    :precondition (and (robot-at ?l) (holding ?i))
    :effect (at ?i ?l)
  )

  (:action release
    :parameters (?i - item)
    :precondition (holding ?i)
    :effect (and (not (holding ?i)) (hand-empty) (clear ?i))
  )

  ;; ---------- Pouring ----------
  (:action pour
    :parameters (?from - item ?to - item ?l - location)
    :precondition (and (robot-at ?l) (holding ?from)
                        (at ?to ?l) (has-liquid ?from))
    :effect (and (has-liquid ?to) (not (has-liquid ?from)))
  )
)