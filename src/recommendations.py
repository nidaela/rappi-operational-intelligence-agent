"""Recommendation layer for the Rappi restaurants operational-risk MVP."""

import pandas as pd

from src.clean_data import clean_restaurants_data
from src.load_data import load_restaurants_data
from src.scoring import score_restaurants
from src.utils import export_enriched_restaurants


def assign_urgency(risk_level: str) -> str:
    """Map risk level to intervention urgency."""
    urgency_map = {
        "Critical": "Immediate",
        "At Risk": "Soon",
        "Stable": "Low",
    }
    return urgency_map.get(risk_level, "Low")


def build_recommended_action(row: pd.Series) -> str:
    """
    Build a single recommended action using priority rules.
    These are mock operational recommendations for the MVP, not internal Rappi playbooks.
    """
    if row["drop_rating_flag"] == 1 and row["complaint_spike_flag"] == 1:
        return (
            "Contact the partner today to review customer experience issues and recent "
            "complaints."
        )
    if row["high_cancel_flag"] == 1:
        return (
            "Review menu availability, prep flow, and operational bottlenecks with the "
            "partner."
        )
    if row["order_drop_flag"] == 1:
        return (
            "Review recent operational changes and monitor commercial impact over the "
            "next 48 hours."
        )
    if row["delivery_delay_flag"] == 1:
        return (
            "Check preparation and delivery bottlenecks and align on corrective actions "
            "with the partner."
        )
    if row["low_nps_flag"] == 1:
        return (
            "Review recent service quality issues and define a short-term recovery "
            "follow-up plan."
        )
    return "No immediate action required. Keep under routine monitoring."


def add_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add urgency and recommended action fields to scored data.
    Recommendations are MVP mock guidance and not production playbooks.
    """
    recommended_df = df.copy()
    recommended_df["recommended_action"] = recommended_df.apply(
        build_recommended_action, axis=1
    )
    recommended_df["urgency"] = recommended_df["risk_level"].apply(assign_urgency)
    return recommended_df


if __name__ == "__main__":
    raw_df = load_restaurants_data()
    cleaned_df = clean_restaurants_data(raw_df)
    scored_df = score_restaurants(cleaned_df)
    recommended_df = add_recommendations(scored_df)
    output_file = export_enriched_restaurants(recommended_df)

    print(f"DataFrame shape: {recommended_df.shape}")
    print("Counts by urgency:")
    print(recommended_df["urgency"].value_counts())

    preview_cols = [
        "restaurant_id",
        "nombre",
        "risk_level",
        "urgency",
        "risk_drivers",
        "recommended_action",
    ]
    print("First 10 rows (selected columns):")
    print(recommended_df[preview_cols].head(10))
    print(f"Exported file: {output_file}")
