#!/usr/bin/env python3

import pyplanning as pp

domain_file = "domain2.pddl"
problem_file = "problem2.pddl"

domain, problem = pp.load_pddl(domain_file, problem_file)
plan = pp.solvers.search_plan(problem)

if plan is not None:
    print("Plan found:")
    print(plan, "\n")
else:
    print("Planning failed.")
