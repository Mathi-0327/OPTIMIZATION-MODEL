import pandas as pd
import pulp
import os

def load_data():
    supply_df = pd.read_csv("data/raw/supply.csv")
    demand_df = pd.read_csv("data/raw/demand.csv")
    cost_df = pd.read_csv("data/raw/transport_cost.csv")

    return supply_df, demand_df, cost_df


def preprocess_data(supply_df, demand_df, cost_df):
    # Convert to dictionaries
    supply = dict(zip(supply_df["Factory"], supply_df["Supply"]))
    demand = dict(zip(demand_df["Warehouse"], demand_df["Demand"]))

    cost = {}
    for _, row in cost_df.iterrows():
        cost[(row["Factory"], row["Warehouse"])] = row["Cost_per_Unit"]

    # Save merged data into processed folder
    merged_df = cost_df.merge(supply_df, on="Factory").merge(demand_df, on="Warehouse")

    os.makedirs("data/processed", exist_ok=True)
    merged_df.to_csv("data/processed/merged_data.csv", index=False)

    return supply, demand, cost, merged_df


def build_and_solve_model(supply, demand, cost):
    factories = list(supply.keys())
    warehouses = list(demand.keys())

    model = pulp.LpProblem("Supply_Chain_Transportation_Optimization", pulp.LpMinimize)

    # Decision variables
    x = pulp.LpVariable.dicts("Ship", [(f, w) for f in factories for w in warehouses],
                              lowBound=0, cat="Continuous")

    # Objective function
    model += pulp.lpSum([cost[(f, w)] * x[(f, w)] for f in factories for w in warehouses])

    # Supply constraints
    for f in factories:
        model += pulp.lpSum([x[(f, w)] for w in warehouses]) <= supply[f], f"Supply_Constraint_{f}"

    # Demand constraints
    for w in warehouses:
        model += pulp.lpSum([x[(f, w)] for f in factories]) >= demand[w], f"Demand_Constraint_{w}"

    # Solve
    model.solve()

    return model, x


def generate_reports(model, x, supply, demand, cost):
    factories = list(supply.keys())
    warehouses = list(demand.keys())

    # Optimal shipping plan
    shipping_plan = []
    for f in factories:
        for w in warehouses:
            shipped_units = x[(f, w)].value()
            shipping_plan.append([f, w, shipped_units, cost[(f, w)], shipped_units * cost[(f, w)]])

    shipping_df = pd.DataFrame(shipping_plan, columns=[
        "Factory", "Warehouse", "Units_Shipped", "Cost_per_Unit", "Total_Cost"
    ])

    # Total cost
    total_cost = pulp.value(model.objective)

    # Factory utilization report
    factory_utilization = []
    for f in factories:
        used = shipping_df[shipping_df["Factory"] == f]["Units_Shipped"].sum()
        remaining = supply[f] - used
        utilization_percent = (used / supply[f]) * 100
        factory_utilization.append([f, supply[f], used, remaining, utilization_percent])

    utilization_df = pd.DataFrame(factory_utilization, columns=[
        "Factory", "Supply_Available", "Units_Shipped", "Remaining_Supply", "Utilization_%"
    ])

    # Warehouse demand report
    warehouse_report = []
    for w in warehouses:
        received = shipping_df[shipping_df["Warehouse"] == w]["Units_Shipped"].sum()
        extra = received - demand[w]
        warehouse_report.append([w, demand[w], received, extra])

    warehouse_df = pd.DataFrame(warehouse_report, columns=[
        "Warehouse", "Demand", "Units_Received", "Extra_or_Shortage"
    ])

    # Save outputs
    os.makedirs("outputs", exist_ok=True)

    shipping_df.to_csv("outputs/optimal_shipping_plan.csv", index=False)
    utilization_df.to_csv("outputs/resource_utilization.csv", index=False)
    warehouse_df.to_csv("outputs/warehouse_demand_report.csv", index=False)

    # Total cost report
    cost_report = pd.DataFrame({"Total_Transportation_Cost": [total_cost]})
    cost_report.to_csv("outputs/total_cost_report.csv", index=False)

    return total_cost, shipping_df, utilization_df, warehouse_df


def main():
    print("Loading data...")
    supply_df, demand_df, cost_df = load_data()

    print("Preprocessing data...")
    supply, demand, cost, merged_df = preprocess_data(supply_df, demand_df, cost_df)

    print("Building and solving optimization model...")
    model, x = build_and_solve_model(supply, demand, cost)

    print("Generating reports...")
    total_cost, shipping_df, utilization_df, warehouse_df = generate_reports(model, x, supply, demand, cost)

    print("\nOptimization Completed Successfully!")
    print("Minimum Total Transportation Cost: ₹", total_cost)

    print("\nFiles Generated in outputs/:")
    print("- optimal_shipping_plan.csv")
    print("- resource_utilization.csv")
    print("- warehouse_demand_report.csv")
    print("- total_cost_report.csv")

    print("\nProcessed file generated:")
    print("- data/processed/merged_data.csv")


if __name__ == "__main__":
    main()
