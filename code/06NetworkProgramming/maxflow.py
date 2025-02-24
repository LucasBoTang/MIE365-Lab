# define graph: nodes and edges with distances
nodes = ["S", "A", "B", "T"]
edges, capacities = gp.multidict({
    ("S", "A"): 10,
    ("S", "B"): 5,
    ("A", "B"): 5,
    ("A", "T"): 5,
    ("B", "T"): 10
})

# create model
m = gp.Model("MaxFlow")

# TODO: decision variables: flow on each edge (bounded by capacity)
x = m.addVars(edges, lb=0, ub=capacities, vtype=GRB.CONTINUOUS, name="x")

# TODO: objective: maximize total flow from S
m.setObjective(gp.quicksum(x["S", j] for j in nodes if ("S", j) in edges), GRB.MAXIMIZE)

# TODO: Flow conservation constraints for all intermediate nodes
m.addConstrs((gp.quicksum(x[j, i] for j in nodes if (j, i) in edges) ==
              gp.quicksum(x[i, k] for k in nodes if (i, k) in edges)
              for i in nodes if i not in ["S", "T"]), "flow_balance")

# Solve model
m.optimize()

# Print results
if m.status == GRB.OPTIMAL:
    print(f"\nMaximum Flow: {m.objVal}")
    print("Flow distribution:")
    for i, j in edges:
        print(f"  Flow on {i} → {j}: {x[i, j].x}")
