(define (domain robotic-object-serving)

  (:requirements :strips :typing)

  (:types
    object   ; manipulable items (mug, bowl, etc.)
    location ; symbolic places the robot/objects can be at
  )

  (:predicates
    (robot-at ?l - location)          ; robot's current location
    (at ?o - object ?l - location)    ; object o is resting at location l
    (in ?o1 - object ?o2 - object)    ; object o1 is contained inside object o2
    (holding ?o - object)             ; gripper is currently holding o
    (gripper-empty)                   ; gripper holds nothing
    (positioned ?o - object)          ; o has been placed at a target location but not yet released
  )

  ; ---------------------------------------------------------------
  ; Move the robot between two symbolic locations
  ; ---------------------------------------------------------------
  (:action move
    :parameters (?from - location ?to - location)
    :precondition (and (robot-at ?from))
    :effect (and
              (not (robot-at ?from))
              (robot-at ?to))
  )

  ; ---------------------------------------------------------------
  ; Remove an object from inside a container it is nested in
  ; (e.g., taking the mug out of the bowl)
  ; ---------------------------------------------------------------
  (:action remove
    :parameters (?o - object ?c - object ?l - location)
    :precondition (and
                    (robot-at ?l)
                    (gripper-empty)
                    (in ?o ?c)
                    (at ?c ?l))
    :effect (and
              (holding ?o)
              (not (gripper-empty))
              (not (in ?o ?c)))
  )

  ; ---------------------------------------------------------------
  ; Grasp an object that is resting freely at a location
  ; ---------------------------------------------------------------
  (:action grasp
    :parameters (?o - object ?l - location)
    :precondition (and
                    (robot-at ?l)
                    (gripper-empty)
                    (at ?o ?l))
    :effect (and
              (holding ?o)
              (not (gripper-empty))
              (not (at ?o ?l)))
  )

  ; ---------------------------------------------------------------
  ; Position a held object at the robot's current location
  ; (gripper still closed around it)
  ; ---------------------------------------------------------------
  (:action place
    :parameters (?o - object ?l - location)
    :precondition (and
                    (holding ?o)
                    (robot-at ?l))
    :effect (and
              (at ?o ?l)
              (positioned ?o))
  )

  ; ---------------------------------------------------------------
  ; Open the gripper and let go of an already-positioned object
  ; ---------------------------------------------------------------
  (:action release
    :parameters (?o - object)
    :precondition (and
                    (holding ?o)
                    (positioned ?o))
    :effect (and
              (not (holding ?o))
              (gripper-empty)
              (not (positioned ?o)))
  )

)