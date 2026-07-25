#!/usr/bin/env python3

from kstar_planner import planners
from pathlib import Path
from pprint import pprint

domain_file = Path("domain.pddl")
problem_file = Path("problem.pddl")

plans = planners.plan_topk(
    domain_file=domain_file,
    problem_file=problem_file,
    number_of_plans_bound=3,
    timeout=30,
)
pprint(plans)
