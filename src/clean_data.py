"""Data cleaning helpers for the Rappi restaurants dataset."""

import pandas as pd

from src.load_data import load_restaurants_data

NUMERIC_COLUMNS = [
    "rating_actual",
    "rating_prom_30d",
    "delta_rating",
    "tasa_cancelacion_pct",
    "tiempo_entrega_avg_min",
    "ordenes_7d",
    "ordenes_7d_anterior",
    "var_ordenes_pct",
    "quejas_7d",
    "nps_score",
    "valor_ticket_prom_mxn",
]

TEXT_COLUMNS = [
    "kam_asignado",
    "ciudad",
    "vertical",
    "nombre",
    "semaforo_riesgo",
]


def clean_restaurants_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply basic cleaning and typing rules to the restaurants dataframe."""
    cleaned_df = df.copy()

    for col in NUMERIC_COLUMNS:
        if col in cleaned_df.columns:
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors="coerce")

    if "activo_desde" in cleaned_df.columns:
        cleaned_df["activo_desde"] = pd.to_datetime(
            cleaned_df["activo_desde"], errors="coerce"
        )

        # Documented mock-data consistency adjustment:
        # replace year 2027 with 2026 while preserving month/day values.
        mask_2027 = cleaned_df["activo_desde"].dt.year == 2027
        cleaned_df.loc[mask_2027, "activo_desde"] = cleaned_df.loc[
            mask_2027, "activo_desde"
        ].map(lambda d: d.replace(year=2026) if pd.notna(d) else d)

    for col in TEXT_COLUMNS:
        if col in cleaned_df.columns:
            cleaned_df[col] = cleaned_df[col].astype("string").str.strip()

    return cleaned_df


if __name__ == "__main__":
    raw_df = load_restaurants_data()
    cleaned_df = clean_restaurants_data(raw_df)

    print(f"DataFrame shape: {cleaned_df.shape}")
    print("Dtypes:")
    print(cleaned_df.dtypes)

    if "activo_desde" in cleaned_df.columns:
        print(f"Min activo_desde: {cleaned_df['activo_desde'].min()}")
        print(f"Max activo_desde: {cleaned_df['activo_desde'].max()}")
    else:
        print("Min activo_desde: column not found")
        print("Max activo_desde: column not found")

    preview_cols = [
        "restaurant_id",
        "nombre",
        "activo_desde",
        "kam_asignado",
        "semaforo_riesgo",
    ]
    available_preview_cols = [col for col in preview_cols if col in cleaned_df.columns]

    print("First 5 rows (selected columns):")
    print(cleaned_df[available_preview_cols].head(5))
