import gurobipy as gp
from gurobipy import GRB

# define parameters
states = [0, 1, 2, 3] # states

# define allowed actions per state
actions = {
    0: [2, 3, 4],
    1: [1, 2, 3],
    2: [0, 1, 2],
    3: [0, 1]
}

# define transition probabilities P(t | s, a)
P = {
    # s = 0
    (0, 2): {0: 0.5, 1: 0.5},
    (0, 3): {1: 0.5, 2: 0.5},
    (0, 4): {2: 0.5, 3: 0.5},
    # s = 1
    (1, 1): {0: 0.5, 1: 0.5},
    (1, 2): {1: 0.5, 2: 0.5},
    (1, 3): {2: 0.5, 3: 0.5},
    # s = 2
    (2, 0): {0: 0.5, 1: 0.5},
    (2, 1): {1: 0.5, 2: 0.5},
    (2, 2): {2: 0.5, 3: 0.5},
    # s = 3
    (3, 0): {1: 0.5, 2: 0.5},
    (3, 1): {2: 0.5, 3: 0.5}
}

# define the cost with s-a pairs
cost = {
    # s = 0
    (0, 2): 6,
    (0, 3): 7,
    (0, 4): 8,
    # s = 1
    (1, 1): 6,
    (1, 2): 7,
    (1, 3): 8,
    # s = 2
    (2, 0): 2,
    (2, 1): 7,
    (2, 2): 8,
    # s = 3
    (3, 0): 3,
    (3, 1): 8
}

# ceate a model
m = gp.Model("MDP")
# varibles
pi = m.addVars(cost, lb=0, name="steady-state distribution")
# obj func: minimize total expected cost
m.setObjective(gp.quicksum(cost[s_a] * pi[s_a] for s_a in cost), GRB.MINIMIZE)
# constraint
m.addConstrs((gp.quicksum(pi[t, a] for a in actions[t]) ==
              gp.quicksum(P.get((s, a), {}).get(t, 0) * pi[s, a] for s in states for a in actions[s])
             for t in states), name="flow balance")
m.addConstr(pi.sum() == 1, name="normalization")

# solve
m.optimize()
# Output results
print("\nOptimal steady-state policy (pi_sa > 0):")
for (s, a) in cost:
    if pi[s, a].X > 1e-6:
        print(f"State {s}, Action {a} -> π = {pi[s, a].X:.4f}")
