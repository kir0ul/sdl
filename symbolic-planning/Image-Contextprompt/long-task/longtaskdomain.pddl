;; domain.pddl
;; Domain: tabletop manipulation - unstack nested items from a drawer,
;; place them on the table, close the drawer, and pour liquid.

(define (domain table-setup)

  (:requirements :strips :typing :negative-preconditions)

  (:types
    location    ; symbolic places the robot/objects can be (e.g. loc-drawer, loc-table)
    drawer      ; a storage furniture object that can be opened/closed
    item        ; manipulable objects: mug, bowl, bottle, etc.
  )

  (:predicates
    (robot-at ?l - location)                 ; robot's current symbolic location
    (loc-of ?d - drawer ?l - location)        ; static: the drawer is located at ?l
    (table-loc ?l - location)                 ; static: ?l is a table-top placement location
    (hand-empty)                              ; gripper is free
    (holding ?i - item)                       ; gripper is holding ?i
    (nested ?i1 - item ?i2 - item)            ; ?i1 is sitting inside ?i2 (e.g. mug in bowl)
    (inside ?i - item ?d - drawer)            ; ?i is inside drawer ?d
    (open ?d - drawer)                        ; drawer is open
    (closed ?d - drawer)                      ; drawer is closed
    (drawer-empty ?d - drawer)                ; no item remains inside the drawer
    (on-table ?i - item)                      ; ?i currently rests on the table
    (has-liquid ?i - item)                    ; ?i currently contains liquid
  )

  ;; ---------------------------------------------------------------
  ;; Move the robot base/end-effector between symbolic locations
  ;; ---------------------------------------------------------------
  (:action move
    :parameters (?from - location ?to - location)
    :precondition (robot-at ?from)
    :effect (and (not (robot-at ?from)) (robot-at ?to))
  )

  ;; ---------------------------------------------------------------
  ;; Open a closed drawer while standing at its location
  ;; ---------------------------------------------------------------
  (:action open-drawer
    :parameters (?d - drawer ?l - location)
    :precondition (and
        (robot-at ?l)
        (loc-of ?d ?l)
        (closed ?d)
        (hand-empty))
    :effect (and
        (open ?d)
        (not (closed ?d)))
  )

  ;; ---------------------------------------------------------------
  ;; Close an open, empty drawer while standing at its location
  ;; ---------------------------------------------------------------
  (:action close-drawer
    :parameters (?d - drawer ?l - location)
    :precondition (and
        (robot-at ?l)
        (loc-of ?d ?l)
        (open ?d)
        (drawer-empty ?d)
        (hand-empty))
    :effect (and
        (closed ?d)
        (not (open ?d)))
  )

  ;; ---------------------------------------------------------------
  ;; Grasp an item (?i1) that is nested inside another item (?i2),
  ;; where the container ?i2 itself is inside the open drawer ?d.
  ;; e.g. grasp the mug that sits inside the bowl.
  ;; ---------------------------------------------------------------
  (:action grasp-nested
    :parameters (?i1 - item ?i2 - item ?d - drawer ?l - location)
    :precondition (and
        (robot-at ?l)
        (loc-of ?d ?l)
        (open ?d)
        (nested ?i1 ?i2)
        (inside ?i2 ?d)
        (hand-empty))
    :effect (and
        (holding ?i1)
        (not (nested ?i1 ?i2))
        (not (hand-empty)))
  )

  ;; ---------------------------------------------------------------
  ;; Grasp an item directly from inside the open drawer (e.g. the
  ;; now-un-nested bowl). Marks the drawer empty for later closing.
  ;; ---------------------------------------------------------------
  (:action grasp-from-drawer
    :parameters (?i - item ?d - drawer ?l - location)
    :precondition (and
        (robot-at ?l)
        (loc-of ?d ?l)
        (open ?d)
        (inside ?i ?d)
        (hand-empty))
    :effect (and
        (holding ?i)
        (not (inside ?i ?d))
        (drawer-empty ?d)
        (not (hand-empty)))
  )

  ;; ---------------------------------------------------------------
  ;; Grasp an item that is currently resting on the table
  ;; ---------------------------------------------------------------
  (:action grasp-from-table
    :parameters (?i - item ?l - location)
    :precondition (and
        (robot-at ?l)
        (table-loc ?l)
        (on-table ?i)
        (hand-empty))
    :effect (and
        (holding ?i)
        (not (on-table ?i))
        (not (hand-empty)))
  )

  ;; ---------------------------------------------------------------
  ;; Place a held item down onto the table
  ;; ---------------------------------------------------------------
  (:action place-on-table
    :parameters (?i - item ?l - location)
    :precondition (and
        (robot-at ?l)
        (table-loc ?l)
        (holding ?i))
    :effect (and
        (on-table ?i)
        (hand-empty)
        (not (holding ?i)))
  )

  ;; ---------------------------------------------------------------
  ;; Pour liquid from a held source container into a target
  ;; container that is resting on the table
  ;; ---------------------------------------------------------------
  (:action pour
    :parameters (?src - item ?dst - item ?l - location)
    :precondition (and
        (robot-at ?l)
        (table-loc ?l)
        (holding ?src)
        (has-liquid ?src)
        (on-table ?dst))
    :effect (has-liquid ?dst)
  )

)
