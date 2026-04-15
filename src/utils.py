"""Shared utility helpers for MVP I/O operations."""

from pathlib import Path

OUTPUT_PATH = Path("data/output/enriched_restaurants_output.csv")


def export_enriched_restaurants(df):
    """Export enriched restaurants data to CSV and return the destination path."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    return OUTPUT_PATH


# Example usage (from another module):
# output_file = export_enriched_restaurants(enriched_df)
