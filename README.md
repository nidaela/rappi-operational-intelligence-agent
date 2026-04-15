# Rappi Operational Intelligence Agent

## Overview
This MVP supports Key Account Managers (KAMs) in identifying restaurants that need timely operational attention. It processes risk signals from the Rappi AI Builder Challenge Case 02 dataset and converts them into a prioritized view of restaurant health.

Instead of relying only on reactive monitoring, the solution provides an explainable risk layer that highlights where intervention is more urgent. The output is designed to help KAMs focus faster on restaurants with the highest operational risk.

The project includes a lightweight data pipeline and a Streamlit interface to make risk status, drivers, and next actions easy to review.

## Problem
KAMs manage large restaurant portfolios, and monitoring is often reactive. This makes it hard to identify deteriorating partners early and act before performance issues escalate. The challenge requires proactive, actionable alerting to prioritize interventions.

## Solution
This MVP:
- Loads the `Case2_Restaurantes` dataset
- Cleans and standardizes operational fields
- Applies a heuristic scoring model
- Classifies restaurants into `Stable` / `At Risk` / `Critical`
- Generates risk drivers and recommended actions
- Displays results in a multilingual Streamlit app (English, Spanish, Portuguese)

## Stack
- Python
- Pandas
- Streamlit
- Openpyxl

## Workflow
- Load data from the challenge Excel sheet
- Clean and standardize key fields
- Fix 2027 dates to 2026 as a mock-data consistency adjustment
- Compute risk score
- Assign risk level
- Generate risk drivers
- Generate recommended actions
- Export enriched CSV
- Display results in Streamlit

## Scoring Logic
The MVP uses a heuristic scoring model based on six operational dimensions:
- Rating deterioration
- Cancellation rate
- Delivery time
- Order variation
- Complaints
- NPS

Thresholds are heuristic and intended for demo purposes. The model is built to be explainable and transparent, and it is not calibrated as a production-grade risk model.

## Assumptions
- The first Excel row is metadata; the second row contains the actual header
- 2027 dates were interpreted as 2026 for consistency in mock data
- `semaforo_riesgo` is treated as a reference field, not as the source of truth
- Recommendations are mock operational suggestions, not internal Rappi playbooks

## How to Run
```bash
python -m src.recommendations
streamlit run app.py
```

## Output
The enriched dataset is exported to:

`data/output/enriched_restaurants_output.csv`

## Future Improvements
- Calibrate thresholds with historical performance data
- Validate intervention logic with KAM stakeholders
- Segment risk logic by restaurant type and maturity
- Integrate alerts into Slack or email workflows
- Refine recommendations using real operational playbooks
