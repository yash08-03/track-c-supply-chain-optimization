# Prediction-Driven Inventory Allocation Optimization for Multi-Branch Industrial Distribution

**Track:** C – Applied Optimization
**Scenario:** S1 – Supply Chain Risk & Optimization
**Sub-Track:** Prediction-Driven Optimization
**Candidate:** Yash Agarwal
**Project Overview:** https://youtu.be/oxqs9shirMg

## Reproducing Results

1. Install dependencies
2. Run feature engineering
3. Train forecasting models
4. Evaluate models
5. Generate baseline allocation
6. Run optimization
7. Run sensitivity analysis

---

# 1. Problem Statement

Manufacturing and industrial distribution organizations regularly face three major operational challenges:

1. Demand volatility
2. Inventory imbalances across branches
3. Supplier and logistics disruptions

Poor inventory allocation decisions lead to stockouts, excess inventory carrying costs, reduced service levels, and lost revenue.

The objective of this project is to build a prediction-driven optimization pipeline that:

* Forecasts future SKU demand
* Uses forecasts as inputs to an optimization model
* Determines optimal inventory allocation across branches
* Maximizes profitability while respecting operational constraints

This project was developed for **Track C – Applied Optimization**.

The forecasting model is not the primary deliverable. Instead, machine learning outputs are used as inputs to a constrained optimization problem, which aligns directly with the requirements of Track C.

---

# 2. Why This Problem?

I selected the Supply Chain Risk & Optimization scenario because it represents a real-world enterprise decision-making problem where machine learning alone is insufficient.

Forecasts answer:

> "What is likely to happen?"

Optimization answers:

> "What should we do about it?"

Business value is created only when forecasts are converted into actionable decisions.

Therefore, forecasting was treated as a supporting component feeding an optimization model.

---

# 3. Dataset

No dataset was provided as part of the challenge.

A synthetic supply-chain dataset was created to simulate a realistic industrial distribution network.

The dataset includes:

* 100 SKUs
* 8 Branches
* 36 Months of historical demand
* Supplier information
* Inventory levels
* Lead times
* Stockout events
* Transportation costs
* Warehouse capacities
* ABC inventory classification

---

# 4. Synthetic Data Assumptions

The dataset was generated with realistic operational characteristics:

### Demand

Demand contains:

* Seasonality
* Trend effects
* Random variation
* Regional demand differences

### Inventory

Inventory levels fluctuate over time and occasionally trigger stockout events.

### Supplier Risk

Each supplier is assigned a risk score representing disruption likelihood.

### Transportation

Transportation cost indices vary by branch to simulate logistics differences.

### Warehouse Capacity

Each branch has finite storage capacity.

### ABC Classification

Inventory is categorized into:

* A Class (high importance)
* B Class (medium importance)
* C Class (lower importance)

Service-level requirements vary by inventory class.

---

# 5. Solution Architecture

Data Generation
→ Feature Engineering
→ Demand Forecasting
→ Model Evaluation
→ Optimization Formulation
→ Inventory Allocation Optimization
→ Business KPI Reporting

The solution follows a two-stage prediction-driven optimization architecture.

---

# 6. Stage 1: Demand Forecasting

## Feature Engineering

The following features were engineered:

### Time-Based Features

* Month
* Quarter
* Year

### Lag Features

* Lag 1
* Lag 2
* Lag 3
* Lag 6
* Lag 12

### Rolling Statistics

* Rolling Mean (3 months)
* Rolling Mean (6 months)
* Rolling Standard Deviation (3 months)
* Rolling Standard Deviation (6 months)

### Business Features

* Inventory Ratio
* Demand Growth Rate
* Supplier Risk
* Transportation Cost Index
* Lead Time

---

# 7. Forecasting Models

Two forecasting models were evaluated.

## Model 1: Random Forest

Reason for Selection:

* Strong baseline model
* Robust on structured tabular datasets
* Resistant to overfitting
* Easy to interpret

### Results

* RMSE = 6.24
* MAE = 2.03
* MAPE = 2.47%

---

## Model 2: XGBoost

Reason for Selection:

* Captures nonlinear relationships
* Handles feature interactions effectively
* Industry-standard gradient boosting approach

### Results

* RMSE = 5.51
* MAE = 2.76
* MAPE = 3.90%

---

# 8. Why XGBoost Was Selected

The optimization layer depends on forecast quality.

Although Random Forest produced lower MAE and MAPE, XGBoost achieved lower RMSE.

RMSE was selected as the primary metric because larger forecasting errors have a greater impact on downstream inventory decisions.

Therefore:

**Selected Forecasting Model = XGBoost**

---

# 9. Alternative Models Considered

## ARIMA

Rejected because:

* Difficult to incorporate rich operational features
* Less suitable for large SKU-level forecasting problems

## Prophet

Rejected because:

* Strong for business time series
* Less flexible for operational feature integration

## LSTM

Rejected because:

* Increased implementation complexity
* Reduced explainability
* Limited benefit for current dataset size

---

# 10. Stage 2: Inventory Allocation Optimization

The forecasting model provides future demand estimates.

These forecasts become inputs to the optimization model.

This follows the Prediction-Driven Optimization sub-track described in the challenge.

---

# 11. Optimization Formulation

## Decision Variable

x(i,j)

Quantity of SKU i allocated to Branch j.

### Why This Formulation?

Alternative considered:

* Replenishment quantity optimization

Chosen approach:

* Inventory allocation optimization

Reason:

Allocation decisions are directly controllable by planners and have immediate operational impact.

---

## Objective Function

Maximize:

Profit
− Transportation Cost
− Supplier Risk Penalty
− Stockout Cost

Business Interpretation:

Allocate inventory where it generates the highest expected value while minimizing operational risk and logistics costs.

---

# 12. Constraints

## Inventory Availability Constraint

Allocated inventory cannot exceed available inventory.

Business Meaning:

Inventory cannot be allocated if it does not physically exist.

---

## Warehouse Capacity Constraint

Allocated inventory cannot exceed warehouse capacity.

Business Meaning:

Branches have finite storage space.

---

## Service Level Constraint

A-Class Inventory = 98%

B-Class Inventory = 95%

C-Class Inventory = 90%

Business Meaning:

Critical inventory receives higher fulfillment priority.

---

## Demand Constraint

Allocated inventory cannot exceed forecast demand.

Business Meaning:

Avoid unnecessary inventory deployment.

---

# 13. Solver Selection

## Selected

PuLP + CBC Solver

### Why PuLP?

* Fast implementation
* Readable optimization formulation
* Open-source
* Easy reproducibility

---

## Alternative Considered

OR-Tools

Advantages:

* Better scalability
* More advanced optimization support

Trade-off Accepted:

Slightly lower scalability in exchange for simpler implementation and transparency.

---

# 14. Optimization Results

Optimization Status:

**Optimal**

Problem Size:

* 100 SKUs
* 8 Branches
* ~800 Allocation Decisions

Optimization Runtime:

Less than 1 second

Final Optimized Profit:

**$5.91 Million**

Constraint Satisfaction Rate:

**100%**

All hard constraints were satisfied.

---

# 15. Baseline vs Optimized Solution

A rule-based baseline allocation was created using proportional demand allocation.

The optimized solution improved business performance by considering:

* Transportation costs
* Supplier risk
* Capacity constraints
* Service-level requirements

The optimization framework produced a measurable improvement over the rule-based baseline.

---

# 16. Sensitivity Analysis

The following scenarios were evaluated:

### Scenario 1

Demand +20%

### Scenario 2

Demand -20%

### Scenario 3

Capacity +10%

### Scenario 4

Capacity -10%

### Key Insight

Demand forecast quality has a larger effect on profitability than moderate warehouse-capacity changes.

This indicates that forecasting accuracy is the most influential component of the solution.

---

# 17. Constraint Interpretation

Most Binding Constraints:

1. Inventory Availability
2. Warehouse Capacity

### Business Interpretation

Inventory availability directly limits revenue opportunities.

Warehouse capacity becomes a bottleneck only after inventory availability increases.

---

# 18. Production Integration

In a production environment:

ERP System
→ Forecast Pipeline
→ Optimization Engine
→ Allocation Recommendation Engine

Re-optimization would occur:

* Daily
* Weekly
* Or whenever inventory changes materially

---

# 19. Failure Modes

## Failure Mode 1

Forecast Drift

Cause:

Unexpected market changes.

Impact:

Suboptimal inventory allocation.

Mitigation:

Automated retraining and forecast monitoring.

---

## Failure Mode 2

Optimization Infeasibility

Cause:

Conflicting constraints.

Impact:

No feasible solution.

Mitigation:

Soft constraints and penalty-based relaxation.

---

# 20. Scalability Discussion

Current Scale:

* 100 SKUs
* 8 Branches

Runtime:

< 1 second

Expected Scaling Challenge:

At 10,000+ SKUs and hundreds of branches, exact optimization may become computationally expensive.

Potential Future Approaches:

* OR-Tools
* Benders Decomposition
* Column Generation
* Heuristic Optimization

---

# 21. Explainability & Experiment Tracking

Planned Production Enhancements:

* SHAP Analysis for forecast explainability
* MLflow for experiment tracking
* Automated model comparison dashboards

Due to challenge time constraints, model comparison results were tracked through version-controlled metrics files.

---

# 22. Limitations

This implementation intentionally simplifies several real-world factors:

* Deterministic demand forecasts
* Linear cost assumptions
* Single-period optimization
* Synthetic dataset

These simplifications improve tractability while still demonstrating the optimization methodology.

---

# 23. Repository Structure

```text
data/
├── sku_master.csv
├── branch_master.csv
├── monthly_demand.csv

src/
├── feature_engineering.py
├── random_forest_forecast.py
├── xgboost_forecast.py
├── baseline_allocator.py
├── inventory_optimizer.py
├── sensitivity_analysis.py

results/
├── forecasts/
├── metrics/
├── baseline_allocation.csv
├── optimized_allocation.csv
├── optimization_metrics.csv
├── sensitivity_results.csv
├── baseline_vs_optimized.csv
├── shadow_price_report.csv

writeup/
├── technical_writeup.pdf
```

# 24. Reproducibility

Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Run Pipeline

```bash
python src/feature_engineering.py
python src/random_forest_forecast.py
python src/xgboost_forecast.py
python src/baseline_allocator.py
python src/inventory_optimizer.py
python src/sensitivity_analysis.py
```

# 25. Conclusion

This project demonstrates a complete prediction-driven optimization workflow where machine learning forecasts are integrated into a constrained optimization model to support inventory allocation decisions.

The final solution combines forecasting, operational constraints, and optimization techniques to improve inventory planning, reduce operational risk, and maximize profitability``  `````````` in a multi-branch industrial distribution environment.
