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

# master problem creation
master = gp.Model("Benders Master")
# turn off log
master.Params.outputFlag = 0
# first-stage decision variables
planting = master.addVars(planting_cost.keys(), vtype=GRB.CONTINUOUS, name="planting")
# recourse approximation variables
η = master.addVars(scenarios, vtype=GRB.CONTINUOUS, lb=-1e9, name="η")
# objective function for the master problem
planting_cost_total = gp.quicksum(planting[crop] * planting_cost[crop] for crop in planting_cost)
resoucers_total = gp.quicksum(probabilities[sc] * η[sc] for sc in scenarios)
master.setObjective(planting_cost_total + resoucers_total, GRB.MINIMIZE)
# land constraint
master.addConstr(planting.sum() <= land_available, "Land Balance")

# subproblem
def subproblem(scenario, planting):
    # create Gurobi model
    subprob = gp.Model("Subproblem")
    # turn off log
    subprob.Params.outputFlag = 0
    # decision variables
    sales = subprob.addVars(selling_price.keys(), vtype=GRB.CONTINUOUS, name="sales")
    purchase = subprob.addVars(purchase_cost.keys(), vtype=GRB.CONTINUOUS, name="purchases")
    # objective function
    revenue = gp.quicksum(sales[crop] * selling_price[crop] for crop in selling_price)
    purchase_cost_total = gp.quicksum(purchase[crop] * purchase_cost[crop] for crop in purchase_cost)
    subprob.setObjective(- revenue + purchase_cost_total, GRB.MINIMIZE)
    # constraints
    subprob.addConstr(yields[scenario]["wheat"] * planting["wheat"].x + purchase["wheat"] - sales["wheat"] >= feed_requirements["wheat"], "Wheat Balance")
    subprob.addConstr(yields[scenario]["corn"] * planting["corn"].x + purchase["corn"] - sales["corn"] >= feed_requirements["corn"], "Corn Balance")
    subprob.addConstr(yields[scenario]["beets"] * planting["beets"].x - sales["beets_high"] - sales["beets_low"] >= 0, "Beet Balance")
    subprob.addConstr(sales["beets_high"] <= beet_sale_limit, "Beets Limit")
    return subprob

# init cnt
iter = 0
# Bender's decomposition loop
while True:
    # count
    iter += 1
    # initialize a flag to check if any cuts were added
    cuts_added = False
    # solve the master
    master.optimize()
    print(f"Iteration {iter}, Objective Value: {-master.objVal:.0F}")
    for crop in planting:
        print(f"  plant {planting[crop].x:.0f} acres of {crop}.")
    print("\n")
    # for each scenario
    for sc in scenarios:
        # solve subproblem for the current scenario
        subprob = subproblem(sc, planting)
        subprob.optimize()
        # get the objective value of the subproblem
        Q_value = subprob.objVal
        # check adding a cut
        if η[sc].x < Q_value - 1e-6:
            # extract dual variables from subproblem constraints
            dual_wheat = subprob.getConstrByName("Wheat Balance").pi
            dual_corn = subprob.getConstrByName("Corn Balance").pi
            dual_beets = subprob.getConstrByName("Beet Balance").pi
            dual_beets_limit = subprob.getConstrByName("Beets Limit").pi
            # formulate the cut using dual values and add it to the master problem
            cut_expr = dual_wheat * (feed_requirements["wheat"] - yields[sc]["wheat"] * planting["wheat"]) \
                     + dual_corn * (feed_requirements["corn"] - yields[sc]["corn"] * planting["corn"]) \
                     + dual_beets * (- yields[sc]["beets"] * planting["beets"]) \
                     + dual_beets_limit * (beet_sale_limit)
            master.addConstr(η[sc] >= cut_expr, f"BendersCut {sc} at Iter {iter}")
            cuts_added = True
    # if no new cuts are added, stop the loop
    if not cuts_added:
        print("Convergence reached. No more cuts needed.")
        break

# display the results
print(f"\nNet profit: {-master.objVal:.0f}")
for crop in planting:
    print(f"  plant {planting[crop].x:.0f} acres of {crop}.")
