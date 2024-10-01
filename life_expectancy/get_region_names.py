import pandas as pd
import pycountry

# Load the data into a DataFrame
df = pd.read_csv('data/eu_life_expectancy_raw.tsv', sep='\t')

# Assuming regions are stored in the first column before cleaning
regions = df.iloc[:, 0].str.split(',', expand=True)[3].unique()
print(regions)

# Manual mapping for special region codes
manual_country_mapping = {
    'UK': 'United Kingdom',
    'XK': 'Kosovo',
    'EL': 'Greece',          # Add EL for Greece
    'FX': 'Metropolitan France'  # Add FX for Metropolitan France
    # Add any other special cases you encounter
}

def get_country_name(region_code):
    # Check if the region_code is in the manual mapping first
    if region_code in manual_country_mapping:
        return manual_country_mapping[region_code]
    
    # Otherwise, use pycountry for standard ISO codes
    country = pycountry.countries.get(alpha_2=region_code)
    if country:
        return country.name
    else:
        return 'Unknown'
    
# After extracting region abbreviations, map them to country names
regions = df.iloc[:, 0].str.split(',', expand=True)[3].unique()
mapped_regions = {region: get_country_name(region) for region in regions}
print(mapped_regions)