"""Utilities for loading the Rappi restaurants dataset from Excel."""

from pathlib import Path

import pandas as pd

# Path to the challenge dataset Excel file.
DATA_PATH = Path("data/input/Rappi_AI_Builder_Challenge_Dataset.xlsx")

# Sheet to load from the Excel workbook.
SHEET_NAME = "Caso2_Restaurantes"


def load_restaurants_data() -> pd.DataFrame:
    """Load the restaurants sheet from the configured Excel dataset."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset file not found at '{DATA_PATH}'. "
            "Place the Excel file in data/input/ and try again."
        )

    try:
        # The first row in this sheet is metadata/title; actual column headers are on row 2.
        df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME, header=1)
        df = df.dropna(axis=1, how="all")
        df.columns = df.columns.astype(str).str.strip()
        return df
    except ValueError as exc:
        # pandas raises ValueError when the sheet name is not found.
        raise ValueError(
            f"Sheet '{SHEET_NAME}' was not found in '{DATA_PATH}'."
        ) from exc
    except Exception as exc:
        # Catch unexpected read errors and provide context.
        raise RuntimeError(
            f"Failed to load Excel data from '{DATA_PATH}' (sheet '{SHEET_NAME}')."
        ) from exc


if __name__ == "__main__":
    try:
        df = load_restaurants_data()
        print(f"DataFrame shape: {df.shape}")
        print("Columns:")
        print(df.columns.tolist())
        print("First 5 rows:")
        print(df.head(5))
    except Exception as exc:
        print(f"Error loading dataset: {exc}")
