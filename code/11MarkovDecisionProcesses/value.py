import gurobipy as gp
from gurobipy import GRB

# define parameters
states = [0, 1, 2, 3] # states
beta = 0.8 # discounted factor

def valueIterationUpdate(V, beta):
    V_new = {}
    # state = 0 and a in (2, 3, 4)
    V_new[0] = min(6 + beta * (0.5 * V[0] + 0.5 * V[1]),
                   7 + beta * (0.5 * V[1] + 0.5 * V[2]),
                   8 + beta * (0.5 * V[2] + 0.5 * V[3]))
    # state = 1 and a in (1, 2, 3)
    V_new[1] = min(6 + beta * (0.5 * V[0] + 0.5 * V[1]),
                   7 + beta * (0.5 * V[1] + 0.5 * V[2]),
                   8 + beta * (0.5 * V[2] + 0.5 * V[3]))
    # state = 2 and a in (0, 1, 2)
    V_new[2] = min(2 + beta * (0.5 * V[0] + 0.5 * V[1]),
                   7 + beta * (0.5 * V[1] + 0.5 * V[2]),
                   8 + beta * (0.5 * V[2] + 0.5 * V[3]))
    # state = 3 and a in (0, 1)
    V_new[3] = min(3 + beta * (0.5 * V[1] + 0.5 * V[2]),
                   8 + beta * (0.5 * V[2] + 0.5 * V[3]))
    return V_new

# init value
V = {0:0, 1:0, 2:0, 3:0}

# iterations
for it in range(100):
    V = valueIterationUpdate(V, beta)
    print(f"Value after iteration {it+1}:", {k: round(v, 2) for k, v in V.items()})
