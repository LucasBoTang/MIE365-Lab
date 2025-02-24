# define nodes
nodes = ["Warehouse1", "Warehouse2", "Retailer1", "Retailer2"]

# define supply and demand at each node (positive = supply, negative = demand)
supply_demand = {
    "Warehouse1": 20,  # Warehouse 1 supplies 20 units
    "Warehouse2": 30,  # Warehouse 2 supplies 30 units
    "Retailer1": -25,  # Retailer 1 requires 25 units
    "Retailer2": -25   # Retailer 2 requires 25 units
}

# define edges with (capacity, cost per unit)
edges, capacities, costs = gp.multidict({
    ("Warehouse1", "Retailer1"): [15, 4],  # (capacity, cost)
    ("Warehouse1", "Retailer2"): [10, 3],
    ("Warehouse2", "Retailer1"): [20, 3],
    ("Warehouse2", "Retailer2"): [15, 1],
    ("Retailer1", "Retailer2"): [10, 5]
})

# Create Gurobi model
m = gp.Model("MinCostFlow")

# TODO: decision variables: flow on each edge
x = m.addVars(edges, lb=0, ub=capacities, obj=costs, vtype=GRB.CONTINUOUS, name="flow")

# TODO: flow constraints: Inflow - Outflow
m.addConstrs(
    (gp.quicksum(x[i, j] for j in nodes if (i, j) in edges) -
     gp.quicksum(x[j, i] for j in nodes if (j, i) in edges) == supply_demand[i]
     for i in nodes),
    "flow_balance"
)

# slve model
m.optimize()

# print results
if m.status == GRB.OPTIMAL:
    print(f"\nMinimum Cost: {m.objVal}")
    print("Optimal Transportation Plan:")
    for i, j in edges:
        if x[i, j].x > 0:
            print(f"  Send {x[i, j].x:.0f} units from {i} to {j}")
