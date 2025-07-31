# OPTIMIZATION PROBLEM: OPTIMAL PRODUCTION PLAN FOR ALPHA MANUFACTURING CO.

# --- Problem Description ---

# Alpha Manufacturing Co. produces two types of products: Product A and Product B.
# The company aims to determine the optimal number of units to produce for each product
# to maximize its total profit, considering limited resources.

# Each product consumes different amounts of raw materials, labor hours, and machine hours.

# Resource Requirements and Availability:
# | Resource      | Product A (per unit) | Product B (per unit) | Available Capacity |
# | :------------ | :------------------- | :------------------- | :----------------- |
# | Raw Material  | 2 kg                 | 3 kg                 | 120 kg             |
# | Labor Hours   | 3 hours              | 2 hours              | 100 hours          |
# | Machine Hours | 1 hour               | 1 hour               | 45 hours           |
# | Profit        | $50                  | $60                  |                    |

# --- Mathematical Formulation ---

# Let:
# x_A = Number of units of Product A to produce
# x_B = Number of units of Product B to produce

# Objective Function (Maximize Profit):
# Maximize Z = 50 * x_A + 60 * x_B

# Constraints:
# 1. Raw Material Constraint: 2 * x_A + 3 * x_B <= 120
# 2. Labor Hours Constraint: 3 * x_A + 2 * x_B <= 100
# 3. Machine Hours Constraint: 1 * x_A + 1 * x_B <= 45
# 4. Non-negativity Constraint: x_A >= 0, x_B >= 0

# --- Solution using PuLP ---

# First, install PuLP if you haven't already:
# !pip install pulp

import pulp

# 1. Create the LP problem
# We want to maximize, so we use LpMaximize
problem = pulp.LpProblem("Alpha_Manufacturing_Production_Plan", pulp.LpMaximize)

# 2. Define Decision Variables
# We define our variables with a lower bound of 0 (cannot produce negative units)
# and as integers, as we assume we produce whole units of products.
x_A = pulp.LpVariable("Product_A", lowBound=0, cat='Integer')
x_B = pulp.LpVariable("Product_B", lowBound=0, cat='Integer')

# 3. Add the Objective Function to the problem
problem += 50 * x_A + 60 * x_B, "Total Profit"

# 4. Add the Constraints to the problem
problem += 2 * x_A + 3 * x_B <= 120, "Raw Material Constraint"
problem += 3 * x_A + 2 * x_B <= 100, "Labor Hours Constraint"
problem += 1 * x_A + 1 * x_B <= 45, "Machine Hours Constraint"

# 5. Solve the problem
problem.solve()

# 6. Check the status of the solution
print(f"Status: {pulp.LpStatus[problem.status]}\n")

# 7. Print the optimal values of the decision variables
print("Optimal Production Quantities:")
for v in problem.variables():
    print(f"{v.name} = {v.varValue}")

# 8. Print the maximum profit
print(f"\nMaximum Total Profit = ${pulp.value(problem.objective)}")

# --- Insights ---

# Let's verify which constraints are binding (fully utilized) and which have slack.
print("\nConstraint Analysis:")
for name, constraint in problem.constraints.items():
    print(f"{name}:")
    # The slack is the difference between the right-hand side and the left-hand side at the optimal solution
    lhs_value = pulp.value(constraint.expr)
    rhs_value = constraint.constant * -1 # For <= constraints, constant is negative
    slack = rhs_value - lhs_value
    print(f"  Left Hand Side (LHS) = {lhs_value}")
    print(f"  Right Hand Side (RHS) = {rhs_value}")
    print(f"  Slack = {slack}")
    if abs(slack) < 1e-6: # Use a small tolerance for floating point comparisons
        print(f"  This constraint is BINDING (fully utilized).")
    else:
        print(f"  This constraint has SLACK (not fully utilized).")
    print("-" * 30)

print("\nDetailed Insights from Optimal Solution:")
print(f"- To maximize profit, Alpha Manufacturing Co. should produce {int(x_A.varValue)} units of Product A and {int(x_B.varValue)} units of Product B.")
print(f"- This production plan will yield a maximum total profit of ${pulp.value(problem.objective):,.2f}.")

# Analyze binding constraints to identify bottlenecks
binding_constraints = []
for name, constraint in problem.constraints.items():
    lhs_value = pulp.value(constraint.expr)
    rhs_value = constraint.constant * -1
    slack = rhs_value - lhs_value
    if abs(slack) < 1e-6:
        binding_constraints.append(name)

if binding_constraints:
    print(f"- The following resources are fully utilized (bottlenecks): {', '.join(binding_constraints)}.")
    print("  This means that increasing the capacity of these resources could potentially lead to even higher profits.")
else:
    print("- No constraints are fully utilized. This suggests there might be excess capacity in all resources at the current production levels.")

print("- Specifically:")
print(f"  - Raw Material: {pulp.value(2 * x_A + 3 * x_B)} kg used out of 120 kg available. Slack: {120 - pulp.value(2 * x_A + 3 * x_B)} kg.")
print(f"  - Labor Hours: {pulp.value(3 * x_A + 2 * x_B)} hours used out of 100 hours available. Slack: {100 - pulp.value(3 * x_A + 2 * x_B)} hours.")
print(f"  - Machine Hours: {pulp.value(1 * x_A + 1 * x_B)} hours used out of 45 hours available. Slack: {45 - pulp.value(1 * x_A + 1 * x_B)} hours.")

print("\nStrategic Recommendations:")
if "Raw Material Constraint" in binding_constraints:
    print("- Consider sourcing more raw materials or finding more efficient ways to use them, as this is a bottleneck.")
if "Labor Hours Constraint" in binding_constraints:
    print("- Explore options to increase labor availability (e.g., overtime, hiring, automation) if feasible, as labor hours are fully consumed.")
if "Machine Hours Constraint" in binding_constraints:
    print("- Evaluate machine capacity. If this is consistently a bottleneck, investing in more machinery or optimizing machine usage could be beneficial.")
if not binding_constraints:
    print("- The current production levels do not fully utilize all resources. This might indicate an opportunity to introduce new products or increase demand for existing ones if the market allows, or re-evaluate resource allocation.")