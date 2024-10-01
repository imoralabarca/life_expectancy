"""Tests for the cleaning module"""
from pathlib import Path
import pandas as pd
from life_expectancy.cleaning import load_data, clean_data, save_data

input_path = Path(__file__).parent.parent / "data" / "eu_life_expectancy_raw.tsv"
output_path = Path(__file__).parent.parent / "data" / "pt_life_expectancy.csv"


def test_clean_data(pt_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""
    # Load data
    df = load_data(input_path)
    assert df is not None

    df_cleaned = clean_data(df, "PT")
    save_data(df_cleaned, output_path)

    pt_life_expectancy_actual = pd.read_csv(output_path)

    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )
