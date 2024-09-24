import gurobipy as gp
from gurobipy import GRB

# =============================== staisfication ===============================
print("Check if all targets can be satisfied.")
# init model
model = gp.Model("Staisfication")

# decision variables
H = model.addVar(name="head")
C = model.addVar(name="chuck")
M = model.addVar(name="mutton")
W = model.addVar(name="water")
# deviational variables
Fp = model.addVar(name="additional fat")
Fm = model.addVar(name="reduced fat")
Pp = model.addVar(name="additional protein")
Pm = model.addVar(name="reduced protein")
Cp = model.addVar(name="additional cost")
Cm = model.addVar(name="reduced cost")

# target constraints
model.addConstr(0.05 * H + 0.24 * C + 0.11 * M ==   8 + Fp - Fm, name="fat")
model.addConstr(0.20 * H + 0.26 * C + 0.08 * M ==  25 + Pp - Pm, name="protein")
model.addConstr(0.12 * H +    9 * C +    8 * M == 800 + Cp - Cm, name="cost")
model.addConstr(H + C + M + W == 100, name="weight")

# obj func
model.setObjective(Fp + Pm + Cp, sense=GRB.MINIMIZE)

# solves
model.optimize()
# solution
print("Objective Value: {:.2f}".format(model.ObjVal))
print(f"H: {H.x:6.2f} lbs of head.")
print(f"C: {C.x:6.2f} lbs of chuck.")
print(f"M: {M.x:6.2f} lbs of mutton.")
print(f"W: {W.x:6.2f} lbs of water.")
print(f"Fat content is {8+Fp.x-Fm.x:.2f}%.")
print(f"Protein content is {25+Pp.x-Pm.x:.2f}%.")
print(f"Cost is {800+Cp.x-Cm.x:.2f} cent.")
if model.ObjVal < 1e-7:
    print("All targets can be satisfied together.")
print(f"F+: Additional fat is {Fp.x:.4f} lbs")
print(f"P-: Reduced protein is {Pm.x:.4f} lbs")
print(f"C+: Additional cost is {Cp.x:.4f} lbs")
print()

# =============================== Weighted Goal ===============================
protein_tolerance = Pm.x
print(Pm.x)

# init model
model = gp.Model("Weighted LP Goal")

# decision variables
H = model.addVar(name="head")
C = model.addVar(name="chuck")
M = model.addVar(name="mutton")
W = model.addVar(name="water")
# deviational variables
Fp = model.addVar(name="additional fat")
Fm = model.addVar(name="reduced fat")
Pp = model.addVar(name="additional protein")
Pm = model.addVar(name="reduced protein")
Cp = model.addVar(name="additional cost")
Cm = model.addVar(name="reduced cost")

# target constraints
model.addConstr(0.05 * H + 0.24 * C + 0.11 * M ==   8 + Fp - Fm, name="fat")
model.addConstr(0.20 * H + 0.26 * C + 0.08 * M ==  25 + Pp - Pm, name="protein")
model.addConstr(0.12 * H +    9 * C +    8 * M == 800 + Cp - Cm, name="cost")
model.addConstr(H + C + M + W == 100, name="weight")
model.addConstr(Fp == 0, name="no more fat")
model.addConstr(Pm <= protein_tolerance, name="no less protein")
model.addConstr(Cp == 0, name="no more cost")

# obj func
model.setObjective(0.1 * Fm + 0.8 * Pp + 1 * Cm, sense=GRB.MAXIMIZE)

# solves
model.optimize()
# solution
print("Objective Value: {:.2f}".format(model.ObjVal))
print(f"H: {H.x:6.2f} lbs of head.")
print(f"C: {C.x:6.2f} lbs of chuck.")
print(f"M: {M.x:6.2f} lbs of mutton.")
print(f"W: {W.x:6.2f} lbs of water.")
print(f"Fat content is {8+Fp.x-Fm.x:.2f}%.")
print(f"Protein content is {25+Pp.x-Pm.x:.2f}%.")
print(f"Cost is {800+Cp.x-Cm.x:.2f} cent.")
