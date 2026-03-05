(define (domain kitchen_robot)
  (:requirements :strips :typing)
  (:types physobj)
  
  (:predicates 
    (on ?obj - physobj ?surface - physobj)
    (on-table ?obj - physobj) ;; For goal requirement
    (inside-drawer ?obj - physobj)
    (clear ?obj - physobj)
    (drawer-open)
    (drawer-closed)
    (holding ?obj - physobj)
    (hand-empty)
    (poured ?from - physobj ?to - physobj)
  )

  (:action open-drawer
    :parameters ()
    :precondition (drawer-closed)
    :effect (and (drawer-open) (not (drawer-closed))))

  (:action close-drawer
    :parameters ()
    :precondition (and (drawer-open) (hand-empty))
    :effect (and (drawer-closed) (not (drawer-open))))

  ;; SINGLE GRASP ACTION (Strips-compatible)
  ;; This action specifically handles taking an object OFF another object
  (:action grasp-from-object
    :parameters (?obj - physobj ?from - physobj)
    :precondition (and (hand-empty) (clear ?obj) (on ?obj ?from)
                       (or (on-table ?obj) (and (inside-drawer ?obj) (drawer-open))))
    :effect (and (holding ?obj) (not (hand-empty)) (not (clear ?obj)) 
                 (not (on ?obj ?from)) (clear ?from) 
                 (not (on-table ?obj)) (not (inside-drawer ?obj))))

  ;; SINGLE GRASP ACTION (For objects just sitting on the table/drawer alone)
  (:action grasp-simple
    :parameters (?obj - physobj)
    :precondition (and (hand-empty) (clear ?obj)
                       (or (on-table ?obj) (and (inside-drawer ?obj) (drawer-open))))
    :effect (and (holding ?obj) (not (hand-empty)) (not (clear ?obj))
                 (not (on-table ?obj)) (not (inside-drawer ?obj))))

  (:action place-on-table
    :parameters (?obj - physobj)
    :precondition (holding ?obj)
    :effect (and (on-table ?obj) (hand-empty) (clear ?obj) (not (holding ?obj))))

  (:action pour
    :parameters (?bottle - physobj ?cup - physobj)
    :precondition (and (holding ?bottle) (on-table ?cup))
    :effect (poured ?bottle ?cup))
)
