# define graph: nodes and edges with distances
nodes = ["A", "B", "C", "D"]
edges, distances = gp.multidict({
    ("A", "B"): 4,
    ("A", "C"): 2,
    ("B", "C"): 1,
    ("C", "D"): 3
})

# create model
m = gp.Model("ShortestPath")

# decision variables: Flow on each edge
x = m.addVars(edges, lb=0, ub=1, vtype=GRB.CONTINUOUS, name="x")

# objective: Minimize total distance traveled
m.setObjective(gp.quicksum(distances[i, j] * x[i, j] for i, j in edges), GRB.MINIMIZE)

# TODO:constraints
m.addConstr(gp.quicksum(x["A", j] for j in nodes if ("A", j) in edges) == 1, "source")  # supply
m.addConstr(gp.quicksum(x[i, "D"] for i in nodes if (i, "D") in edges) == 1, "sink")    # demand
m.addConstrs((gp.quicksum(x[i, j] for j in nodes if (i, j) in edges) ==
              gp.quicksum(x[j, i] for j in nodes if (j, i) in edges)
              for i in nodes if i not in ["A", "D"]), "flow_balance")  # flow conservation

# solve model
m.optimize()

# print results
if m.status == GRB.OPTIMAL:
    print(f"\nOptimal Distance: {m.objVal}")
    print("Edges used in the shortest path:")
    for i, j in edges:
        if x[i, j].x > 0.5:
            print(f"  {i} → {j}")
