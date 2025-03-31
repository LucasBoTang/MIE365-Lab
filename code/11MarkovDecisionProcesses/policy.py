import gurobipy as gp
from gurobipy import GRB

# define parameters
states = [0, 1, 2, 3] # states
beta = 0.8 # discounted factor

# first interation
print("Iteration 1:")

# evaluation
m = gp.Model("Eval")
# turn off output log
m.setParam("OutputFlag", 0)
# varibles
v = m.addVars(states, lb=-GRB.INFINITY, name="value")
# linear equations
m.addConstr(v[0] == 6 + beta * (0.5 * v[0] + 0.5 * v[1]))
m.addConstr(v[1] == 6 + beta * (0.5 * v[0] + 0.5 * v[1]))
m.addConstr(v[2] == 2 + beta * (0.5 * v[0] + 0.5 * v[1]))
m.addConstr(v[3] == 3 + beta * (0.5 * v[1] + 0.5 * v[2]))
# dummy objective (we just want feasibility)
m.setObjective(0, GRB.MINIMIZE)
# solve
m.optimize()
V = {s: v[s].X for s in states}
print("Value after first evaluation:", {k: round(v, 2) for k, v in V.items()})

# improvement
policy = {}
# state = 0 and a in (2, 3, 4)
pi0 = {2: 6 + beta * (0.5 * V[0] + 0.5 * V[1]),
       3: 7 + beta * (0.5 * V[1] + 0.5 * V[2]),
       4: 8 + beta * (0.5 * V[2] + 0.5 * V[3])}
policy[0] = min(pi0, key=pi0.get)
# state = 1 and a in (1, 2, 3)
pi1 = {1: 6 + beta * (0.5 * V[0] + 0.5 * V[1]),
       2: 7 + beta * (0.5 * V[1] + 0.5 * V[2]),
       3: 8 + beta * (0.5 * V[2] + 0.5 * V[3])}
policy[1] = min(pi1, key=pi1.get)
# state = 2 and a in (0, 1, 2)
pi2 = {0: 2 + beta * (0.5 * V[0] + 0.5 * V[1]),
       1: 7 + beta * (0.5 * V[1] + 0.5 * V[2]),
       2: 8 + beta * (0.5 * V[2] + 0.5 * V[3])}
policy[2] = min(pi2, key=pi2.get)
# state = 3 and a in (0, 1)
pi3 = {0: 3 + beta * (0.5 * V[1] + 0.5 * V[2]),
       1: 8 + beta * (0.5 * V[2] + 0.5 * V[3])}
policy[3] = min(pi3, key=pi3.get)
print("Policy after first improvement:", {k: round(v, 2) for k, v in policy.items()})

# second interation
print("\nIteration 2:")

# evaluation
m = gp.Model("Eval")
# turn off output log
m.setParam("OutputFlag", 0)
# varibles
v = m.addVars(states, lb=-GRB.INFINITY, name="value")
# linear equations
m.addConstr(v[0] == 8 + beta * (0.5 * v[2] + 0.5 * v[3]))
m.addConstr(v[1] == 8 + beta * (0.5 * v[2] + 0.5 * v[3]))
m.addConstr(v[2] == 2 + beta * (0.5 * v[0] + 0.5 * v[1]))
m.addConstr(v[3] == 3 + beta * (0.5 * v[1] + 0.5 * v[2]))
# dummy objective (we just want feasibility)
m.setObjective(0, GRB.MINIMIZE)
# solve
m.optimize()
V = {s: v[s].X for s in states}
print("Value after second evaluation:", {k: round(v, 2) for k, v in V.items()})

# improvement
policy = {}
# state = 0 and a in (2, 3, 4)
pi0 = {2: 6 + beta * (0.5 * V[0] + 0.5 * V[1]),
       3: 7 + beta * (0.5 * V[1] + 0.5 * V[2]),
       4: 8 + beta * (0.5 * V[2] + 0.5 * V[3])}
policy[0] = min(pi0, key=pi0.get)
# state = 1 and a in (1, 2, 3)
pi1 = {1: 6 + beta * (0.5 * V[0] + 0.5 * V[1]),
       2: 7 + beta * (0.5 * V[1] + 0.5 * V[2]),
       3: 8 + beta * (0.5 * V[2] + 0.5 * V[3])}
policy[1] = min(pi1, key=pi1.get)
# state = 2 and a in (0, 1, 2)
pi2 = {0: 2 + beta * (0.5 * V[0] + 0.5 * V[1]),
       1: 7 + beta * (0.5 * V[1] + 0.5 * V[2]),
       2: 8 + beta * (0.5 * V[2] + 0.5 * V[3])}
policy[2] = min(pi2, key=pi2.get)
# state = 3 and a in (0, 1)
pi3 = {0: 3 + beta * (0.5 * V[1] + 0.5 * V[2]),
       1: 8 + beta * (0.5 * V[2] + 0.5 * V[3])}
policy[3] = min(pi3, key=pi3.get)
print("Policy after second improvement:", {k: round(v, 2) for k, v in policy.items()})
