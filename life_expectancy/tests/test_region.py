import pytest
from life_expectancy.enums import Region

def test_actual_countries():
    # Get the actual list of countries from the class method
    actual_countries = Region.actual_countries()
    print(actual_countries)

    # Dynamically generate the expected list of countries, excluding special regions
    non_country_regions = {"EU28", "EFTA", "EEA", "EA", "EU27_2020", "EU27_2007", "EEA31", "EEA30_2007", "EA19", "EA18", "DE_TOT"}
    expected_countries = [region for region in Region if region.name not in non_country_regions]
    
    # Assert that the actual countries match the expected countries
    assert actual_countries == expected_countries