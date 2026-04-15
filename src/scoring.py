"""Heuristic MVP scoring model for restaurant operational risk."""

import pandas as pd

from src.clean_data import clean_restaurants_data
from src.load_data import load_restaurants_data


def score_delta_rating(value: float) -> int:
    if pd.isna(value):
        return 0
    if value >= -0.2:
        return 0
    if -0.5 <= value < -0.2:
        return 10
    return 25


def score_tasa_cancelacion_pct(value: float) -> int:
    if pd.isna(value):
        return 0
    if value < 5:
        return 0
    if 5 <= value <= 10:
        return 10
    return 20


def score_tiempo_entrega_avg_min(value: float) -> int:
    if pd.isna(value):
        return 0
    if value < 35:
        return 0
    if 35 <= value <= 50:
        return 8
    return 15


def score_var_ordenes_pct(value: float) -> int:
    if pd.isna(value):
        return 0
    if value > -10:
        return 0
    if -25 <= value <= -10:
        return 10
    return 20


def score_quejas_7d(value: float) -> int:
    if pd.isna(value):
        return 0
    if 0 <= value <= 2:
        return 0
    if 3 <= value <= 5:
        return 5
    return 10


def score_nps_score(value: float) -> int:
    if pd.isna(value):
        return 0
    if value > 50:
        return 0
    if 30 <= value <= 50:
        return 5
    return 10


def classify_risk(row: pd.Series) -> str:
    """Classify baseline risk level from the total risk score."""
    if row["risk_score"] <= 24:
        return "Stable"
    if row["risk_score"] <= 59:
        return "At Risk"
    return "Critical"


def has_critical_override(row: pd.Series) -> bool:
    """Force Critical for severe combined-signal scenarios."""
    if row["risk_score"] < 45:
        return False

    condition_1 = row["delta_rating"] < -0.5 and row["tasa_cancelacion_pct"] > 10
    condition_2 = row["var_ordenes_pct"] < -25 and row["quejas_7d"] > 5
    condition_3 = row["nps_score"] < 30 and row["delta_rating"] < -0.5
    return bool(condition_1 or condition_2 or condition_3)


def build_risk_drivers(row: pd.Series) -> str:
    """Build up to 3 primary risk drivers from active flags."""
    driver_map = [
        ("drop_rating_flag", "Strong rating drop"),
        ("high_cancel_flag", "High cancellation rate"),
        ("delivery_delay_flag", "Delivery delays"),
        ("order_drop_flag", "Order volume decline"),
        ("complaint_spike_flag", "Complaint spike"),
        ("low_nps_flag", "Low NPS"),
    ]

    active_drivers = [label for flag, label in driver_map if int(row.get(flag, 0)) == 1]
    if not active_drivers:
        return "No major risk signals"
    return ", ".join(active_drivers[:3])


def score_restaurants(df: pd.DataFrame) -> pd.DataFrame:
    """
    Heuristic MVP scoring for the challenge dataset.
    This is not a calibrated production model.
    """
    scored_df = df.copy()

    scored_df["rating_score"] = scored_df["delta_rating"].apply(score_delta_rating)
    scored_df["cancel_score"] = scored_df["tasa_cancelacion_pct"].apply(
        score_tasa_cancelacion_pct
    )
    scored_df["delivery_score"] = scored_df["tiempo_entrega_avg_min"].apply(
        score_tiempo_entrega_avg_min
    )
    scored_df["orders_score"] = scored_df["var_ordenes_pct"].apply(score_var_ordenes_pct)
    scored_df["complaints_score"] = scored_df["quejas_7d"].apply(score_quejas_7d)
    scored_df["nps_risk_score"] = scored_df["nps_score"].apply(score_nps_score)

    scored_df["drop_rating_flag"] = (scored_df["delta_rating"] < -0.2).astype(int)
    scored_df["high_cancel_flag"] = (scored_df["tasa_cancelacion_pct"] >= 5).astype(int)
    scored_df["delivery_delay_flag"] = (
        scored_df["tiempo_entrega_avg_min"] >= 35
    ).astype(int)
    scored_df["order_drop_flag"] = (scored_df["var_ordenes_pct"] <= -10).astype(int)
    scored_df["complaint_spike_flag"] = (scored_df["quejas_7d"] >= 3).astype(int)
    scored_df["low_nps_flag"] = (scored_df["nps_score"] <= 50).astype(int)

    score_columns = [
        "rating_score",
        "cancel_score",
        "delivery_score",
        "orders_score",
        "complaints_score",
        "nps_risk_score",
    ]
    scored_df["risk_score"] = scored_df[score_columns].sum(axis=1)
    scored_df["risk_level"] = scored_df.apply(classify_risk, axis=1)

    critical_override_mask = scored_df.apply(has_critical_override, axis=1)
    scored_df.loc[critical_override_mask, "risk_level"] = "Critical"

    scored_df["risk_drivers"] = scored_df.apply(build_risk_drivers, axis=1)

    return scored_df


if __name__ == "__main__":
    raw_df = load_restaurants_data()
    cleaned_df = clean_restaurants_data(raw_df)
    scored_df = score_restaurants(cleaned_df)

    print(f"DataFrame shape: {scored_df.shape}")
    print("Counts by risk_level:")
    print(scored_df["risk_level"].value_counts())

    preview_cols = [
        "restaurant_id",
        "nombre",
        "risk_score",
        "risk_level",
        "risk_drivers",
        "semaforo_riesgo",
    ]
    print("First 10 rows (selected columns):")
    print(scored_df[preview_cols].head(10))
