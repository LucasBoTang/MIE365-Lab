# parameters
reliabilities = {
    "A": [0, 0.5, 0.6, 0.8],
    "B": [0, 0.6, 0.7, 0.8],
    "C": [0, 0.7, 0.8, 0.9],
    "D": [0, 0.5, 0.7, 0.9]
}
costs = {
    "A": [0, 100, 200, 300],
    "B": [0, 200, 400, 500],
    "C": [0, 100, 300, 400],
    "D": [0, 200, 300, 400]
}

# indices
components = ["A", "B", "C", "D"]
units = [1, 2, 3]

# recursive dynamic programming function
def dp(comp_ind, budget, memo={}):
    # bsase case: no components left
    if comp_ind >= len(components):
        return 1, []
    # check if solution already computed in memo
    if (comp_ind, budget) in memo:
        return memo[comp_ind, budget]
    # init setting
    max_reliability = 0
    best_units = []
    c = components[comp_ind]
    # recursive case: try all unit options for the current component
    for u in units:
        cost = costs[c][u]
        # check if feasible
        if budget >= cost:
            # recursive dp
            reliability, units_used = dp(comp_ind + 1,
                                         budget - cost,
                                         memo)
            current_reliability = reliability * reliabilities[c][u]
            # get best one
            if current_reliability > max_reliability:
                max_reliability = current_reliability
                best_units = [u] + units_used
    # memoize
    memo[comp_ind, budget] = max_reliability, best_units
    # return the result
    return max_reliability, best_units

# solve
max_reliability, unit_configuration = dp(comp_ind=0, budget=1000)

# solution
print("Solutions:")
obj_val = 1
for i, c in enumerate(components):
    print("Component {}: {} units.".format(c, unit_configuration[i]))
print("Maximum Reliability: {:.4f}".format(max_reliability))
