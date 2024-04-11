import pytest
from src.weather_data import WeatherData  

@pytest.fixture
def mock_units_converter(mocker):
    mock = mocker.patch("src.utility.units_converter")
    mock.return_value = (23.0, 25.0, 5.0) 
    return mock

def test_wind_speed_adjustment_within_limits():
    # Test that wind speed is adjusted within the applicability limits
    weather = WeatherData(dry_bulb_temp=30, radiant_temp=30, wind_speed=0.3, relative_humidity=50)
    assert weather.wind_speed == 0.5, "Wind speed should be adjusted to the minimum limit"

    weather = WeatherData(dry_bulb_temp=30, radiant_temp=30, wind_speed=18, relative_humidity=50)
    assert weather.wind_speed == 17, "Wind speed should be adjusted to the maximum limit"

def test_wind_speed_not_adjusted_within_limits():
    # Test that wind speed is not adjusted if it's within the limits
    wind_speed = 5
    weather = WeatherData(dry_bulb_temp=30, radiant_temp=30, wind_speed=wind_speed, relative_humidity=50)
    assert weather.wind_speed == wind_speed, "Wind speed should remain as provided"

def test_units_conversion_to_si(mock_units_converter):
    # Test that units are converted to SI if initially in IP
    weather = WeatherData(dry_bulb_temp=86, radiant_temp=90, wind_speed=10, relative_humidity=50, units="IP")
    assert weather.units == "SI", "Units should be converted to SI"
    assert weather.dry_bulb_temp == 30.0, "Dry bulb temperature should be converted to SI units"
    assert round(weather.radiant_temp, 2) == 32.22, "Radiant temperature should be converted to SI units"
    assert round(weather.wind_speed, 2) == 3.05, "Wind speed should be converted to SI units"

def test_no_units_conversion_when_already_si():
    # Test that no conversion happens if units are already SI
    initial_values = (30, 30, 5)
    weather = WeatherData(dry_bulb_temp=initial_values[0], radiant_temp=initial_values[1], wind_speed=initial_values[2], relative_humidity=50, units="SI")
    assert weather.dry_bulb_temp == initial_values[0], "Dry bulb temperature should remain unchanged"
    assert weather.radiant_temp == initial_values[1], "Radiant temperature should remain unchanged"
    assert weather.wind_speed == initial_values[2], "Wind speed should remain unchanged"
