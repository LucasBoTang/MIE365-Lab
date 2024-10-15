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

# solve the LP with expected yields
m = gp.Model("Simple Approach")
# decision variables
planting = m.addVars(planting_cost.keys(), vtype=GRB.CONTINUOUS, name="plants")
sales = m.addVars(selling_price.keys(), vtype=GRB.CONTINUOUS, name="sales")
purchase = m.addVars(purchase_cost.keys(), vtype=GRB.CONTINUOUS, name="purchases")
# objective function
revenue = gp.quicksum(sales[crop] * selling_price[crop] for crop in selling_price)
planting_cost_total = gp.quicksum(planting[crop] * planting_cost[crop] for crop in planting_cost)
purchase_cost_total = gp.quicksum(purchase[crop] * purchase_cost[crop] for crop in purchase_cost)
m.setObjective(revenue - planting_cost_total - purchase_cost_total, GRB.MAXIMIZE)
# constraints
m.addConstr(expected_yields["wheat"] * planting["wheat"] + purchase["wheat"] - sales["wheat"] >= feed_requirements["wheat"], "Wheat Balance")
m.addConstr(expected_yields["corn"] * planting["corn"] + purchase["corn"] - sales["corn"] >= feed_requirements["corn"], "Corn Balance")
m.addConstr(expected_yields["beets"] * planting["beets"] - sales["beets_high"] - sales["beets_low"] >= 0, "Beet Balance")
m.addConstr(sales["beets_high"] <= beet_sale_limit, "Beets Limit")
m.addConstr(planting.sum() <= land_available, "Land Balance")
# solve the model
m.optimize()
# display the results
print(f"\nNet profit: {m.objVal:.0f}")
for crop in planting:
    print(f"  plant {planting[crop].x:.0f} acres of {crop}.")

# evaluate the profit for each scenario
def resouceFunction(scenario, planting):
    # create Gurobi model
    m = gp.Model("Resource Function")
    # decision variables
    sales = m.addVars(selling_price.keys(), vtype=GRB.CONTINUOUS, name="sales")
    purchase = m.addVars(purchase_cost.keys(), vtype=GRB.CONTINUOUS, name="purchases")
    # objective function
    revenue = gp.quicksum(sales[crop] * selling_price[crop] for crop in selling_price)
    planting_cost_total = gp.quicksum(planting[crop].x * planting_cost[crop] for crop in planting_cost)
    purchase_cost_total = gp.quicksum(purchase[crop] * purchase_cost[crop] for crop in purchase_cost)
    m.setObjective(revenue - planting_cost_total - purchase_cost_total, GRB.MAXIMIZE)
    # constraints
    m.addConstr(yields[scenario]["wheat"] * planting["wheat"].x + purchase["wheat"] - sales["wheat"] >= feed_requirements["wheat"], "Wheat Balance")
    m.addConstr(yields[scenario]["corn"] * planting["corn"].x + purchase["corn"] - sales["corn"] >= feed_requirements["corn"], "Corn Balance")
    m.addConstr(yields[scenario]["beets"] * planting["beets"].x - sales["beets_high"] - sales["beets_low"] >= 0, "Beet Balance")
    m.addConstr(sales["beets_high"] <= beet_sale_limit, "Beets Limit")
    return m
# scenario 1
q1 = resouceFunction(1, planting)
q1.optimize()
obj1 = q1.objVal
# scenario 2
q2 = resouceFunction(2, planting)
q2.optimize()
obj2 = q2.objVal
# scenario 3
q3 = resouceFunction(3, planting)
q3.optimize()
obj3 = q3.objVal

# result
print(f"\nProfit for Scenario 1: {obj1:.0f}")
print(f"Profit for Scenario 2: {obj2:.0f}")
print(f"Profit for Scenario 3: {obj3:.0f}")
expected_profit = probabilities[1] * obj1 + probabilities[2] * obj2 + probabilities[3] * obj3
print(f"Expected Profit: {expected_profit:.0f}")
