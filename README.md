# OPTIMIZATION-MODEL

*COMPANY*: CODTECH IT SOLUTIONS

*NAME*: MATHIYAZHAGAN M 

*INTERN ID*: CTIS4317

*DOMAIN*: DATA SCIENCE

*DURATION*: 4 WEEEKS

*MENTOR*: NEELA SANTOSH

## project discription
This project is an internship-level Supply Chain Transportation Optimization Model developed using Linear Programming (LP) with the PuLP library in Python. The goal of this project is to solve a real-world logistics business problem where a company distributes products from multiple factories to multiple warehouses located in different cities.

Each factory has a limited supply capacity, meaning it cannot ship beyond its available production limit. Similarly, each warehouse has a fixed demand requirement that must be fulfilled to maintain smooth operations. Transportation cost varies for every factory-to-warehouse route. The objective of this model is to determine the optimal shipment quantity for each route such that all warehouse demands are satisfied, factory supply limits are not exceeded, and the overall transportation cost is minimized.

The project workflow includes data loading, preprocessing, model formulation, constraint definition, and optimization solving. Decision variables represent the shipment quantity between each factory and warehouse. The objective function minimizes the total transportation cost, while constraints ensure supply and demand conditions are met.

After solving the optimization model, the project generates business-ready output reports and saves them in CSV format. The outputs include:

optimal_shipping_plan.csv: Displays the best shipment quantity from each factory to each warehouse.

resource_utilization.csv: Shows factory supply usage, remaining capacity, and utilization percentage.

warehouse_demand_report.csv: Confirms whether each warehouse demand is satisfied.

total_cost_report.csv: Provides the minimum total transportation cost achieved by the model.

merged_data.csv (processed data): Stores cleaned and merged dataset for analysis.

This project demonstrates how optimization techniques can be applied in real-world supply chain management to reduce logistics cost, improve distribution planning, and support data-driven decision-making.
