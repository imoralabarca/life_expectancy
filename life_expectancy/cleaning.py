import os
import argparse
import re
from pathlib import Path
from typing import Optional
import pandas as pd
from life_expectancy.enums import Region
from life_expectancy.strategies import CSVDataStrategy, JSONDataStrategy, DataStrategy

desired_order = ["unit", "sex", "age", "region", "year", "value"]

def get_data_strategy(file_path: str) -> DataStrategy:
    """Select the appropriate data strategy based on the file extension."""
    _, file_extension = os.path.splitext(file_path)
    if file_extension == '.csv':
        return CSVDataStrategy()
    elif file_extension == '.json':
        return JSONDataStrategy()
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def load_data(file_path):
    """Loads the data from a TSV file and returns a DataFrame."""
    try:
        df = pd.read_csv(file_path, sep="\t")
        print(type(df))  # Add this to debug
        print("Data loaded successfully.")
        return df

    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
        return None


def clean_invalid_characters(value):
    """Removes invalid characters from numeric strings."""
    if isinstance(value, str):
        # Remove any character that is not a digit or decimal point
        value = re.sub(r"[^0-9.]", "", value)
    return value


def clean_data(df, country: Optional[Region] = Region.PT):
    """Cleans the data and filters by the specified country."""
    try:
        df_long = df.melt(id_vars=df.columns[0], var_name="year", value_name="value")
        df_long[["unit", "sex", "age", "region"]] = df_long[df.columns[0]].str.split(
            ",", expand=True
        )
        df_long = df_long.drop(columns=[df.columns[0]])
        df_long["year"] = df_long["year"].astype(int)
        df_long["value"] = df_long["value"].apply(clean_invalid_characters)
        df_long["value"] = pd.to_numeric(df_long["value"])
        df_country = df_long[df_long["region"] == country]
        df_country = df_country.dropna(subset=["value"])
        df_country = df_country[desired_order]

        return df_country

    except Exception as e:
        print(f"An error occurred while cleaning the data: {e}")
        return None


def save_data(df, output_path):
    """Saves the cleaned data to a CSV file."""
    try:
        df.to_csv(output_path, index=False)
        print(f"Data saved to '{output_path}' successfully.")
    except Exception as e:
        print(f"An error occurred while saving the data: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Clean life expectancy data for a specific country."
    )
    parser.add_argument(
        "--country",
        type=str,
        default="PT",
        help="Country code to filter the data (default: PT)",
    )
    args = parser.parse_args()

    # File paths
    data_path = Path(__file__).parent / "data" / "eurostat_life_expect.json"
    output_path = Path(__file__).parent / "data" / f'{args.country.lower()}_life_expectancy_cleaned.csv'

    # Load, clean, and save data using appropriate strategy
    strategy = get_data_strategy(data_path)
    df = strategy.load_data(data_path)
    if df is not None:
        cleaned_data = clean_data(df, country=args.country)
        if cleaned_data is not None:
            strategy.save_data(cleaned_data, output_path)


if __name__ == "__main__":
    main()
