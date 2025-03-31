import gurobipy as gp
from gurobipy import GRB

# define parameters
states = [0, 1, 2, 3] # states
beta = 0.8 # discounted factor

# ceate a model
m = gp.Model("MDP")
# varibles
v = m.addVars(states, lb=-GRB.INFINITY, name="value") # value
# obj func
m.setObjective(v.sum(), sense=GRB.MAXIMIZE)
# constr
# v0 = min x in {2,3,4}
m.addConstr(v[0] <= 6 + 0.4 * v[0] + 0.4 * v[1])  # x=2
m.addConstr(v[0] <= 7 + 0.4 * v[1] + 0.4 * v[2])  # x=3
m.addConstr(v[0] <= 8 + 0.4 * v[2] + 0.4 * v[3])  # x=4
# v1 = min x in {1,2,3}
m.addConstr(v[1] <= 6 + 0.4 * v[0] + 0.4 * v[1])  # x=1
m.addConstr(v[1] <= 7 + 0.4 * v[1] + 0.4 * v[2])  # x=2
m.addConstr(v[1] <= 8 + 0.4 * v[2] + 0.4 * v[3])  # x=3
# v2 = min x in {0,1,2}
m.addConstr(v[2] <= 2 + 0.4 * v[0] + 0.4 * v[1])  # x=0
m.addConstr(v[2] <= 7 + 0.4 * v[1] + 0.4 * v[2])  # x=1
m.addConstr(v[2] <= 8 + 0.4 * v[2] + 0.4 * v[3])  # x=2
# v3 = min x in {0,1}
m.addConstr(v[3] <= 3 + 0.4 * v[1] + 0.4 * v[2])  # x=0
m.addConstr(v[3] <= 8 + 0.4 * v[2] + 0.4 * v[3])  # x=1
# solves
m.optimize()
# value
print("Model Solution:")
for s in states:
    print("v_{} = {:.2f}".format(s, v[s].x), end=" ")
