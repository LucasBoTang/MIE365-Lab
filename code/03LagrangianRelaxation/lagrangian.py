import gurobipy as gp
import numpy as np
from gurobipy import GRB

# parameters
c = np.array([90, 80, 70, 60])
A = np.array([[8, 6, 7, 5]])
b = np.array([80])
D = np.array([[3, 1, 0, 0],
              [2, 1, 0, 0],
              [0, 0, 3, 2],
              [0, 0, 1, 1]])
d = np.array([12, 10, 15, 4])

# =============================== Orignal ===============================

print("Solution check with orignal formulation.\n")

# init model
model = gp.Model("Orignal Production")

# decision variables
x = model.addMVar(len(c), name="steels")

# objective function
model.setObjective(c @ x, sense=GRB.MAXIMIZE)

# constraints
model.addConstr(A @ x <= b)
model.addConstr(D @ x <= d)

# solves
model.optimize()

# solution
print("Objective Value: {:.2f}".format(model.ObjVal))
print(f"H: {x[0].x:5.2f} tons Steel1 from Pike.")
print(f"C: {x[1].x:5.2f} tons Steel2 from Pike.")
print(f"M: {x[2].x:5.2f} tons Steel1 from Quid.")
print(f"W: {x[3].x:5.2f} tons Steel2 from Quid.")
print("\n\n")

# =============================== Lagrangian ===============================

print("Iterations for Lagrangian Relxation.\n")

# init master problem
master = gp.Model("Master Problem")
# turn off log
master.Params.outputFlag = 0
# decision variables
λ = master.addMVar(len(A), name="dual")
z = master.addVar(lb=-GRB.INFINITY, name="z") # z is unsigned
# objective function
master.setObjective(z, sense=GRB.MINIMIZE)

# decompose subproblem
c1, c2 = c[:2], c[2:]
D1, D2 = D[:2,:2], D[2:,2:]
d1, d2 = d[:2], d[2:]
# init subproblem 1
subproblem1 = gp.Model("Subproblem 1")
# turn off log
subproblem1.Params.outputFlag = 0
# decision variables
x1 = subproblem1.addMVar(len(c1), name="steels")
# constraints
subproblem1.addConstr(D1 @ x1 <= d1)
# init subproblem 2
subproblem2 = gp.Model("Subproblem 2")
# turn off log
subproblem2.Params.outputFlag = 0
# decision variables
x2 = subproblem2.addMVar(len(c2), name="steels")
# constraints
subproblem2.addConstr(D2 @ x2 <= d2)

# start with x = 0
xval = np.zeros_like(c)
ub = np.inf
# iterative updates
cnt = 0
while True:
    # count
    cnt +=  1
    # add new constraint master
    master.addConstr(z >= b @ λ + (c - λ @ A) @ xval)
    # solve master for λ
    master.optimize()
    λval = λ.X
    # lower bound
    lb = master.ObjVal
    # terminate condition
    if ub - lb < 1e-6:
        break
    # update subproblems obj
    subproblem1.setObjective((c1 - λval @ A[:,:2]) @ x1, sense=GRB.MAXIMIZE)
    subproblem2.setObjective((c2 - λval @ A[:,2:]) @ x2, sense=GRB.MAXIMIZE)
    # solve the subproblems for x
    subproblem1.optimize()
    subproblem2.optimize()
    xval[:2] = x1.X
    xval[2:] = x2.X
    # upper bound
    ub = b @ λval + (c - λval @ A) @ xval
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
print("Objective Value: {:.2f}".format(model.ObjVal))
print(f"H: {x[0].x:5.2f} tons Steel1 from Pike.")
print(f"C: {x[1].x:5.2f} tons Steel2 from Pike.")
print(f"M: {x[2].x:5.2f} tons Steel1 from Quid.")
print(f"W: {x[3].x:5.2f} tons Steel2 from Quid.")
print("\n\n")
