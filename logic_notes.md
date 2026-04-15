## Data Cleaning Notes

- The `Caso2_Restaurantes` sheet uses the first row as metadata/title and the second row as the actual header.
- The `activo_desde` field contained at least one 2027 date, which was interpreted as 2026 for consistency with the 2026 challenge context.
- This date fix was treated as a mock-data consistency adjustment and documented explicitly.

## Scoring Logic

This MVP uses a heuristic scoring model based on six main signals:
- rating deterioration
- cancellation rate
- delivery time
- order volume variation
- complaints
- NPS

The score is intended for explainability and live demo purposes. It is not a calibrated production model.