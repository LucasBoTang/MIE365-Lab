import gurobipy as gp
import numpy as np
from gurobipy import GRB

# data setup
planting_cost = {"wheat": 150, "corn": 230, "beets": 260}
purchase_cost = {"wheat": 238, "corn": 210}
selling_price = {"wheat": 170, "corn": 150, "beets_high": 36, "beets_low": 10}
feed_requirements = {"wheat": 200, "corn": 240}
land_available = 500
beet_sale_limit = 6000

# scenarios and probabilities
expected_yields = {"wheat": 2.5, "corn": 3, "beets": 20}
scenarios = [1, 2, 3]
yields = {
    1: {crop: yield_val for crop, yield_val in expected_yields.items()},    # Scenario 1: Expected yields
    2: {crop: 1.2 * yield_val for crop, yield_val in expected_yields.items()},  # Scenario 2: 20% higher yields
    3: {crop: 0.8 * yield_val for crop, yield_val in expected_yields.items()}   # Scenario 3: 20% lower yields
}
probabilities = {1: 1/3, 2: 1/3, 3: 1/3}

# create Gurobi model
m = gp.Model("Extensive Form")

# decision variables
planting = m.addVars(planting_cost.keys(), vtype=GRB.CONTINUOUS, name="plants")
purchase = m.addVars(scenarios, purchase_cost.keys(), vtype=GRB.CONTINUOUS, name="purchases")
sales = m.addVars(scenarios, selling_price.keys(), vtype=GRB.CONTINUOUS, name="sales")

# objective function
revenue = gp.quicksum(probabilities[sc] * sales[sc, crop] * selling_price[crop] for crop in selling_price for sc in scenarios)
planting_cost_total = gp.quicksum(planting[crop] * planting_cost[crop] for crop in planting_cost)
purchase_cost_total = gp.quicksum(probabilities[sc] * purchase[sc, crop] * purchase_cost[crop] for crop in purchase_cost for sc in scenarios)
m.setObjective(revenue - planting_cost_total - purchase_cost_total, GRB.MAXIMIZE)

# constraints
m.addConstrs((yields[sc]["wheat"] * planting["wheat"] + purchase[sc, "wheat"] - sales[sc, "wheat"] >= feed_requirements["wheat"]
              for sc in scenarios), "Wheat Balance")
m.addConstrs((yields[sc]["corn"] * planting["corn"] + purchase[sc, "corn"] - sales[sc, "corn"] >= feed_requirements["corn"]
              for sc in scenarios), "Corn Balance")
m.addConstrs((yields[sc]["beets"] * planting["beets"] - sales[sc, "beets_high"] - sales[sc, "beets_low"] >= 0
              for sc in scenarios), "Beet Balance")
m.addConstrs((sales[sc, "beets_high"] <= beet_sale_limit for sc in scenarios), "Beets Limit")
m.addConstr(planting.sum() <= land_available, "Land Balance")

# solve the model
m.optimize()

# display the results
print(f"\nNet profit: {m.objVal:.0f}")
for crop in planting:
    print(f"  plant {planting[crop].x:.0f} acres of {crop}.")
