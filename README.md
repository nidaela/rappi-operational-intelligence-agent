# Rappi Operational Intelligence Agent

Live App: https://rappi-kam-risk-agent.streamlit.app

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

## Why This Is an Agent
This solution is not just a monitoring dashboard. It is an Operational Intelligence Agent because it does more than display restaurant metrics.

The system:
- ingests raw restaurant performance data
- cleans and standardizes the dataset
- applies an explicit risk-scoring logic
- classifies restaurants by severity
- derives human-readable risk drivers
- generates recommended next actions
- exposes prioritized alerts through a live, accessible interface

In other words, it automates the path from signal detection -> decision -> alert generation -> recommended action.

The Streamlit app is the chosen delivery channel for this MVP, but the underlying value comes from the decision pipeline behind it. That pipeline is what makes this an agent-oriented solution rather than a passive reporting interface.

## Tooling Decisions
The implementation was intentionally designed to balance speed, clarity, deployability, and explainability.

- Python was chosen because it allows a fast and readable implementation of the full decision pipeline.
- Pandas was used for structured dataset processing, cleaning, feature handling, and scoring.
- Streamlit was selected because it provides the fastest path to a live, shareable, testable interface for operational review.
- A dashboard was chosen as the alert delivery channel because it allows KAMs to review prioritized alerts by portfolio owner in a single place during live execution.
- Rule-based scoring was chosen instead of a more complex ML or LLM-driven decision layer because the challenge provides a static mock dataset without historical labels, and explainability was critical for live presentation.

This stack was selected to maximize practical value under the challenge constraints while keeping the system easy to inspect, run, and extend.

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

## What I Would Do With More Time
With more time, data access, and business context, I would improve this MVP in five main ways:

- calibrate thresholds using historical outcomes instead of heuristic rules
- validate scoring logic directly with KAM leads and merchant operations stakeholders
- segment thresholds by restaurant maturity, vertical, and strategic importance
- integrate alert delivery into operational channels such as Slack or email
- refine recommendations using real internal playbooks and escalation paths

The current version prioritizes explainability, live execution, and operational usefulness over production-grade calibration.
