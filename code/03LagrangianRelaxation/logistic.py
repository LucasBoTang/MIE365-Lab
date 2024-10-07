import gurobipy as gp
import numpy as np
from gurobipy import GRB

# parameters
cost = np.array([[2, 4, 5],
                 [3, 1, 2]])
inventory = np.array([70, 90])
demand = np.array([60, 50, 40])
capacity = np.array([80, 100])

# =============================== Orignal ===============================

print("Solution check with orignal formulation.\n")

# init model
model = gp.Model("Orignal Production")

# decision variables
x = model.addMVar((2, 3), vtype=GRB.CONTINUOUS, name="x")

# objective function
model.setObjective((cost * x).sum(), GRB.MINIMIZE)

# constraints
model.addConstr(x.sum(axis=1) <= inventory, name="Inventory")
model.addConstr(x.sum(axis=0) >= demand, name="Demand")
model.addConstrs((x[i] <= capacity[i] for i in range(2)), name="Vehicle_Capacity")

# solves
model.optimize()

# solution
print("Objective Value: {:.2f}".format(model.ObjVal))
for i in range(2):
    for j in range(3):
        print(f"x[{i+1},{j+1}] = {x[i,j].X}")
print("\n\n")

# =============================== Lagrangian ===============================

print("Iterations for Lagrangian Relxation.\n")

# init master problem
master = gp.Model("Master Problem")
# turn off log
master.Params.outputFlag = 0
# decision variables
λ = master.addMVar((2,3), name="dual")
z = master.addVar(lb=-GRB.INFINITY, name="z") # z is unsigned
# objective function
master.setObjective(z, sense=GRB.MAXIMIZE)

# init subproblem
subproblem = gp.Model("Subproblem")
# turn off log
subproblem.Params.outputFlag = 0
# decision variables
x = subproblem.addMVar((2, 3), name="x")
# constraints
subproblem.addConstr(x.sum(axis=1) <= inventory, name="Inventory")
subproblem.addConstr(x.sum(axis=0) >= demand, name="Demand")

# start with a feasible x
xval = np.array([[60, 10,  0],
                 [ 0, 40, 40]])
lb = - np.inf
# iterative updates
cnt = 0
while True:
    # count
    cnt +=  1
    # add new constraint master
    master.addConstr(z <= (cost * xval).sum() + \
                          gp.quicksum(λ[i,j] * (xval[i,j] - capacity[i])
                                      for i in range(2) for j in range(3)))
    # solve master for λ
    master.optimize()
    λval = λ.X
    # upper bound
    ub = master.ObjVal
    # terminate condition
    if ub - lb < 1e-6:
        break
    # update subproblems obj
    subproblem.setObjective(((cost - λval) * x).sum(), sense=GRB.MINIMIZE)
    # solve the subproblems for x
    subproblem.optimize()
    xval = x.X
    # lower bound
    lb = (cost * xval).sum() + np.sum(λval[i,j] * (xval[i,j] - capacity[i])
                                      for i in range(2) for j in range(3))
    # terminate
    if ub - lb < 1e-6:
        break
    print(f"Iteration {cnt-1}:")
    print(f"  λ = {λval.tolist()}, Dual Obj = {lb:.2f}.")
    print(f"  x = {xval.tolist()}, Primal Obj = {ub:.2f}.\n")
print(f"Iteration {cnt-1}:")
print(f"  λ = {λval.tolist()}, Dual Obj = {lb:.2f}.")
print(f"  x = {xval.tolist()}, Primal Obj = {ub:.2f}.\n")

# solution
print("Objective Value: {:.2f}".format(master.ObjVal))
for i in range(2):
    for j in range(3):
        print(f"x[{i+1},{j+1}] = {xval[i,j]}")
print("\n\n")
