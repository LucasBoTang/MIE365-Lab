import gurobipy as gp
import numpy as np
from gurobipy import GRB

# available lengths
lengths = [3, 5, 9]
# demand
demand = [25, 20, 15]

# =============================== Orignal ===============================

print("Solution check with orignal formulation.\n")

# wholesale length of copper wire
wholesale_length = 107

# generate all combinations of cutting patterns
def generate_combinations():
    combinations = []
    for a3 in range(wholesale_length // lengths[0] + 1):
        for a5 in range(wholesale_length // lengths[1] + 1):
            for a9 in range(wholesale_length // lengths[2] + 1):
                if (a3 * lengths[0] + a5 * lengths[1] + a9 * lengths[2]) <= wholesale_length:
                    combinations.append((a3, a5, a9))
    return combinations

# generate all possible cutting patterns
patterns = generate_combinations()

# display the number of patterns and a sample
print("Total number of valid cutting patterns:", len(patterns))
print("Sample patterns:", patterns[:10])  # Show first 10 patterns

# create Gurobi model
m = gp.Model("cutting_stock")

# decision variables, one for each cutting pattern
x = m.addVars(len(patterns), vtype=GRB.INTEGER, name="x")

# objective: Minimize the total number of wires used
m.setObjective(gp.quicksum(x[i] for i in range(len(patterns))), GRB.MINIMIZE)

# demand constraints for each length 3 5 9
m.addConstr(gp.quicksum(patterns[i][0] * x[i] for i in range(len(patterns))) >= demand[0], "Demand_3ft")
m.addConstr(gp.quicksum(patterns[i][1] * x[i] for i in range(len(patterns))) >= demand[1], "Demand_5ft")
m.addConstr(gp.quicksum(patterns[i][2] * x[i] for i in range(len(patterns))) >= demand[2], "Demand_9ft")

# optimize the model
m.optimize()

# display the results
if m.status == GRB.OPTIMAL:
    print("\nOptimal solution found:")
    print(f"Minimum number of wires needed: {m.objVal}\n")
    print("Cutting patterns used:")
    for i in range(len(patterns)):
        if x[i].x > 0:
            print(f"Pattern {patterns[i]}: used {x[i].x} times")
else:
    print("No optimal solution found.")

# =============================== Col Gen ===============================

print("Iterations for Column Generation.\n")

# master problem
def solve_master_problem(patterns):
    # create Gurobi model
    m = gp.Model("master")
    # turn off log
    m.Params.outputFlag = 0
    # decision variables for the number of times each pattern is used
    x = m.addVars(len(patterns), vtype=GRB.CONTINUOUS, name="x")
    # objective: Minimize the number of 107' copper wires used
    m.setObjective(gp.quicksum(x[i] for i in range(len(patterns))), GRB.MINIMIZE)
    # constraints to meet demand for each length (3', 5', 9')
    m.addConstr(gp.quicksum(patterns[i][0] * x[i] for i in range(len(patterns))) >= demand[0], "Demand_3ft")
    m.addConstr(gp.quicksum(patterns[i][1] * x[i] for i in range(len(patterns))) >= demand[1], "Demand_5ft")
    m.addConstr(gp.quicksum(patterns[i][2] * x[i] for i in range(len(patterns))) >= demand[2], "Demand_9ft")
    # optimize the master
    m.optimize()
    # objective value
    objval = m.objVal
    # return the dual variables (shadow prices) from the demand constraints
    λ = [m.getConstrByName("Demand_3ft").Pi,
         m.getConstrByName("Demand_5ft").Pi,
         m.getConstrByName("Demand_9ft").Pi]
    return objval, λ

# subproblem
def solve_subproblem(λ):
    # create the subproblem to find new cutting patterns
    m = gp.Model("Subproblem")
    # turn off log
    m.Params.outputFlag = 0
    # decision variables for the number of 3', 5', and 9' lengths
    a3 = m.addVar(vtype=GRB.INTEGER, name="a3")
    a5 = m.addVar(vtype=GRB.INTEGER, name="a5")
    a9 = m.addVar(vtype=GRB.INTEGER, name="a9")
    # objective: maximize the reduced cost (negative of the dual prices)
    m.setObjective(λ[0] * a3 + λ[1] * a5 + λ[2] * a9 - 1, GRB.MAXIMIZE)
    # constraint: less than or equal to whole lengtj
    m.addConstr(3 * a3 + 5 * a5 + 9 * a9 <= wholesale_length, "Length")
    # optimize the subproblem
    m.optimize()
    # objective value
    objval = m.objVal
    # obtain new pattern
    new_pattern = [int(a3.X), int(a5.X), int(a9.X)]
    return objval, new_pattern

# col gen iteration
def column_generation(init_pattern):
    # init patterns
    patterns = [init_pattern]
    cnt = 0
    while True:
        # solve master
        objval, λ = solve_master_problem(patterns)
        # solve subproblem
        rcost, new_pattern = solve_subproblem(λ)
        # if no improvement, break
        if rcost <= 0:
            break
        # add new pattern
        patterns.append(new_pattern)
        cnt += 1
        print(f"Iteration {cnt}: New pattern {new_pattern} with objective value {objval}")
    return patterns

# solve via Col gen
init_pattern = [1, 1, 11]
patterns = column_generation(init_pattern)
# display the number of patterns and a sample
print("Total number of valid cutting patterns:", len(patterns))
print("Patterns:", patterns)

# solve ILP
m = gp.Model("cutting_stock")
# decision variables, one for each cutting pattern
x = m.addVars(len(patterns), vtype=GRB.INTEGER, name="x")
# objective: Minimize the total number of wires used
m.setObjective(gp.quicksum(x[i] for i in range(len(patterns))), GRB.MINIMIZE)
# demand constraints for each length 3 5 9
m.addConstr(gp.quicksum(patterns[i][0] * x[i] for i in range(len(patterns))) >= demand[0], "Demand_3ft")
m.addConstr(gp.quicksum(patterns[i][1] * x[i] for i in range(len(patterns))) >= demand[1], "Demand_5ft")
m.addConstr(gp.quicksum(patterns[i][2] * x[i] for i in range(len(patterns))) >= demand[2], "Demand_9ft")
# optimize the model
m.optimize()
# display the results
print("\nOptimal solution found:")
print(f"Minimum number of wires needed: {m.objVal}\n")
print("Cutting patterns used:")
for i in range(len(patterns)):
    if x[i].x > 0:
        print(f"Pattern {patterns[i]}: used {x[i].x} times")
