import os
import argparse
import re
import pandas as pd

# test

desired_order = ['unit', 'sex', 'age', 'region', 'year', 'value']

def clean_invalid_characters(value):
    """Removes invalid characters from numeric strings."""
    if isinstance(value, str):
        # Remove any character that is not a digit or decimal point
        value = re.sub(r'[^0-9.]', '', value)
    return value

def clean_data(country='PT'):

    data_path = os.path.join(os.path.dirname(__file__), 'data', 'eu_life_expectancy_raw.tsv')
    df = pd.read_csv(data_path, sep='\t')
    print("Data loaded successfully.")
    df_long = df.melt(id_vars=df.columns[0], var_name='year', value_name='value')
    df_long[['unit', 'sex', 'age', 'region']] = df_long[df.columns[0]].str.split(',', expand=True)
    df_long = df_long.drop(columns=[df.columns[0]])
    df_long['year'] = df_long['year'].astype(int)
    df_long['value'] = df_long['value'].apply(clean_invalid_characters)
    df_long['value'] = pd.to_numeric(df_long['value'])
    df_country = df_long[df_long['region'] == country]
    df_country = df_country.dropna(subset=['value'])
    df_country = df_country[desired_order]
    output_path = os.path.join(os.path.dirname(__file__), 'data',
                               f'{country.lower()}_life_expectancy.csv')
    df_country.to_csv(output_path, index=False)
    print(f"Data saved to '{country.lower()}_life_expectancy.csv' successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
                                     "Clean life expectancy data for a specific country.")
    parser.add_argument('--country', type=str, default='PT',
                        help='Country code to filter the data (default: PT)')
    args = parser.parse_args()

    clean_data(country=args.country)