(define (domain manipulation)
  (:requirements :strips :typing :disjunctive-preconditions)
  
  (:types
    object
    container
  )

  (:predicates
    (on-table ?o - object)
    (inside-drawer ?o - object ?d - container)
    (on-top-of ?o1 - object ?o2 - object)
    (open ?d - container)
    (closed ?d - container)
    (hand-empty)
    (holding ?o - object)
    (poured)
  )

(:action grasp
  :parameters (?o - object ?d - container)
  :precondition (and
    (hand-empty)
    (or
      (on-table ?o)
      (and
        (inside-drawer ?o ?d)
        (open ?d)
      )
    )
  )
  :effect (and
    (holding ?o)
    (not (hand-empty))
    (not (on-table ?o))
    (not (inside-drawer ?o ?d))
  )
)

  ;; Place an object on the table
  (:action place-on-table
    :parameters (?o - object)
    :precondition (holding ?o)
    :effect (and
      (on-table ?o)
      (hand-empty)
      (not (holding ?o))
    )
  )

  ;; Open the drawer
  (:action sliding-open
    :parameters (?d - container)
    :precondition (closed ?d)
    :effect (and
      (open ?d)
      (not (closed ?d))
    )
  )

  ;; Close the drawer
  (:action sliding-close
    :parameters (?d - container)
    :precondition (open ?d)
    :effect (and
      (closed ?d)
      (not (open ?d))
    )
  )

  ;; Pour from bottle into cup
  (:action pouring
    :parameters (?b - object ?c - object)
    :precondition (and
      (on-table ?b)
      (on-table ?c)
    )
    :effect (poured)
  )
)
