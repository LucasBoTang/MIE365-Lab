import gurobipy as gp
from gurobipy import GRB
import numpy as np

# parameters
reliabilities = {
    "A": [0, 0.5, 0.6, 0.8],
    "B": [0, 0.6, 0.7, 0.8],
    "C": [0, 0.7, 0.8, 0.9],
    "D": [0, 0.5, 0.7, 0.9]
}
costs = {
    "A": [0, 100, 200, 300],
    "B": [0, 200, 400, 500],
    "C": [0, 100, 300, 400],
    "D": [0, 200, 300, 400]
}

# ceate a model
m = gp.Model("System Reliability")

# indices for 2D variables
components = ["A", "B", "C", "D"]
units = [1, 2, 3]
# variables
x = m.addVars(components, units, vtype=GRB.BINARY, name="x")

# obj func P_A * P_B * P_C * P_D -> log P_A + log P_B + log P_C + log P_D
obj = gp.quicksum(np.log(reliabilities[c][u]) * x[c,u] for c, u in x)
m.setObjective(obj, sense=GRB.MAXIMIZE)

# unit configuration constraints
m.addConstrs(x.sum(c, "*") == 1 for c in components)
# budget constraint
m.addConstr(gp.quicksum(costs[c][u] * x[c,u] for c, u in x) <= 1000)

# solves
m.optimize()

# solution
print()
print("Solutions:")
obj_val = 1
for c, u in x:
    if x[c,u].x >= 1 - 1e-3:
        print("Component {}: {} units.".format(c, u))
        obj_val *= reliabilities[c][u]
print("Maximum Reliability: {:.4f}".format(obj_val))
