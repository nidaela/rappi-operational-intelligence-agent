# Operational Logic Notes

## 1. Data Source
The MVP uses the `Caso2_Restaurantes` sheet from the challenge Excel file (`data/input/Rappi_AI_Builder_Challenge_Dataset.xlsx`).

During ingestion, the first row was treated as metadata/title, and the second row was used as the actual column header (`header=1`).

## 2. Data Preparation
Main cleaning steps applied before scoring:
- Numeric conversion (`errors="coerce"`) for all scoring-related fields.
- Whitespace trimming for key text fields (`kam_asignado`, `ciudad`, `vertical`, `nombre`, `semaforo_riesgo`).
- Datetime parsing for `activo_desde`.
- Year correction from `2027` to `2026` as a mock-data consistency adjustment while preserving month/day.

## 3. Signals Used
Primary risk signals:
- `delta_rating`: change in current rating vs. rolling reference.
- `tasa_cancelacion_pct`: operational cancellations pressure.
- `tiempo_entrega_avg_min`: delivery-time friction.
- `var_ordenes_pct`: commercial demand variation.
- `quejas_7d`: short-term complaint pressure.
- `nps_score`: customer advocacy/satisfaction indicator.

Contextual fields used for display and actionability:
- `restaurant_id`
- `nombre`
- `ciudad`
- `vertical`
- `kam_asignado`
- `activo_desde`
- `semaforo_riesgo`

## 4. Scoring Logic
The MVP uses an explicit heuristic scoring model with fixed thresholds:

- `delta_rating`
  - `>= -0.2 -> 0`
  - `< -0.2 and >= -0.5 -> 10`
  - `< -0.5 -> 25`
- `tasa_cancelacion_pct`
  - `< 5 -> 0`
  - `5 to 10 -> 10`
  - `> 10 -> 20`
- `tiempo_entrega_avg_min`
  - `< 35 -> 0`
  - `35 to 50 -> 8`
  - `> 50 -> 15`
- `var_ordenes_pct`
  - `> -10 -> 0`
  - `<= -10 and >= -25 -> 10`
  - `< -25 -> 20`
- `quejas_7d`
  - `0 to 2 -> 0`
  - `3 to 5 -> 5`
  - `> 5 -> 10`
- `nps_score`
  - `> 50 -> 0`
  - `30 to 50 -> 5`
  - `< 30 -> 10`

`risk_score` is computed as the sum of the six components above.

## 5. Risk Classification
Base classification thresholds:
- `Stable`: `risk_score <= 24`
- `At Risk`: `risk_score <= 59`
- `Critical`: `risk_score >= 60`

Severity override (force `Critical`) applies only if `risk_score >= 45` and at least one condition is true:
- `delta_rating < -0.5` and `tasa_cancelacion_pct > 10`
- `var_ordenes_pct < -25` and `quejas_7d > 5`
- `nps_score < 30` and `delta_rating < -0.5`

## 6. Risk Drivers
The app builds human-readable drivers from active risk flags. Possible outputs include:
- Strong rating drop
- High cancellation rate
- Delivery delays
- Order volume decline
- Complaint spike
- Low NPS
- No major risk signals

## 7. Recommended Actions
Recommended actions are generated through simple rule-based dominance logic. These are mock operational suggestions for the MVP, not internal Rappi playbooks.

Priority order:
- Rating drop + complaint spike
- High cancellation
- Order drop
- Delivery delays
- Low NPS
- Otherwise: routine monitoring

## 8. Output Design
The selected delivery channel is a lightweight Streamlit dashboard because it supports:
- Global prioritization
- KAM-level filtering
- Drill-down by restaurant
- Multilingual display
- Fast alert review during the live presentation

The pipeline also exports an enriched artifact to:
`data/output/enriched_restaurants_output.csv`

## Why This Qualifies as an Operational Intelligence Agent
This MVP was designed as an Operational Intelligence Agent, not as a static monitoring dashboard.

A dashboard typically presents information and leaves interpretation to the user. This solution goes further by automating the operational reasoning layer:

1. it ingests raw restaurant performance data
2. it applies a structured cleaning and standardization process
3. it evaluates multiple signals together instead of relying on a single KPI
4. it computes a risk score
5. it classifies severity
6. it derives human-readable drivers
7. it generates recommended operational actions
8. it exposes alerts in a usable review channel

This means the system does not only visualize data. It transforms raw signals into prioritized operational decisions with recommended next steps. That decision-making layer is the core characteristic that makes this solution agent-like.

## Tooling and Architecture Decisions
The implementation choices were made deliberately to optimize for speed, clarity, explainability, and live-demo reliability.

### Why Python
Python was chosen because it is well suited for fast implementation of data-processing pipelines and transparent business logic.

### Why Pandas
Pandas was used because the challenge is centered on structured tabular data. It allowed fast cleaning, transformation, scoring, and export of the enriched dataset.

### Why Streamlit
Streamlit was chosen because it made it possible to deploy a real, testable, shareable interface quickly. This aligns well with the challenge expectation of a functional and accessible solution.

### Why a dashboard as the alert channel
The challenge allows the notification channel to be chosen freely. For this MVP, a lightweight dashboard was selected because it enables:
- global prioritization
- KAM-level filtering
- live inspection of generated alerts
- restaurant drill-down during presentation
- multilingual display for a LatAm operational context

### Why heuristic scoring
The scoring model was implemented as an explicit rule-based system because:
- the dataset is mock data
- no historical labels or production outcomes were provided
- explainability is important for design review
- the challenge values business judgment, not only statistical optimization

## Explicit Assumptions and Justifications
Several assumptions were required to complete the MVP under challenge constraints.

- The first row of the Excel sheet was treated as metadata and the second row as the actual header because the raw file structure indicated a title row before the dataset columns.
- Dates in 2027 were interpreted as 2026 because the challenge context is 2026 and those records appeared to be mock-data inconsistencies rather than meaningful future dates.
- `semaforo_riesgo` was treated as a reference field, not as source of truth because the challenge explicitly states that the field is reference only and can be redefined by the agent.
- Thresholds were defined heuristically because no historical calibration dataset or production outcomes were provided.
- Recommended actions were written as mock operational suggestions because no internal Rappi playbooks or ownership matrices were provided.
- The dashboard was chosen as the alert delivery channel because the challenge allows a free channel choice and this format is the fastest to deploy, review, and demonstrate live.

## 10. Limitations
This MVP:
- Is not calibrated using historical production outcomes.
- Does not segment thresholds by restaurant type or maturity.
- Does not use internal operational playbooks.
- Does not yet integrate with Slack/email or internal systems.
- Uses heuristic scoring rather than validated predictive modeling.

## If More Time, Team, and Resources Were Available
If more time, stakeholder access, and production context were available, the next steps would be:

### Data and calibration
- calibrate thresholds using historical outcomes
- analyze false positives and false negatives
- compare model output against real partner deterioration or churn patterns

### Business validation
- review the scoring logic with KAM leads
- validate threshold choices with merchant operations stakeholders
- refine alert severity definitions with operational owners

### Recommendation quality
- map each dominant risk pattern to a more specific intervention playbook
- define who owns each action: KAM, operations, merchant support, or another team
- add SLA expectations and escalation paths

### Product and platform
- deliver alerts through Slack or email instead of dashboard-only review
- add execution logs and run history
- store prior outputs to compare risk evolution over time
- introduce alert acknowledgement and follow-up tracking

### Segmentation
- adapt scoring by vertical
- differentiate new vs. mature restaurants
- account for strategic account importance and operational context

## Stakeholders I Would Consult to Close Key Assumptions
To improve this MVP into a production-grade operational agent, I would validate assumptions with the following roles:

- KAM Lead / Partnerships Lead
  to understand which signals really drive intervention priority and what a useful alert looks like in practice

- Merchant Operations Manager
  to refine thresholds, escalation logic, and operational actionability

- Project Manager or Product Manager for the restaurant domain
  to validate workflow fit, expected usage, and downstream process integration

- Business Analyst / Analytics Manager
  to calibrate the scoring model against historical performance patterns and outcomes

- Merchant Support / Partner Success stakeholders
  to align recommended actions with realistic intervention playbooks

## Next Steps to Scale the Solution
The MVP can be scaled in the following sequence:

1. stabilize the current pipeline with historical calibration
2. validate thresholds and recommendations with business stakeholders
3. segment logic by restaurant profile and strategic value
4. deliver alerts through operational channels such as Slack or email
5. add persistence, logging, and run history
6. incorporate feedback loops from KAM usage
7. evolve from heuristic scoring to a hybrid model if validated data becomes available

## 12. Implementation Note
The deployed app is resilient to missing precomputed artifacts because it can regenerate the enriched dataset automatically if the CSV is unavailable.
