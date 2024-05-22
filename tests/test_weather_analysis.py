import pytest
import json
from unittest.mock import patch, MagicMock
from src.weather_analysis import UTCICalculator
from src.data_objects import WeatherData

@pytest.fixture
def weather_data():
    return WeatherData(
        dry_bulb_temp=MagicMock(average=25.0),
        wind_speed=MagicMock(average=1.5),
        wind_direction=MagicMock(),
        relative_humidity=MagicMock(average=60.0),
        radiant_temp=MagicMock(average=30.0),
        total_sky_cover=MagicMock()
    )

@pytest.fixture
def mock_categories(mocker):
    categories = {
        "STRESS_CATEGORIES": {
        "-13, null": "extreme cold stress",
        "0, 9": "no thermal stress",
        "9, 26": "moderate heat stress",
        "26, null": "extreme heat stress"
        },
        "COMFORT_RATINGS": {
        "-13, null": "very uncomfortable",
        "0, 9": "slightly uncomfortable",
        "9, 26": "comfortable",
        "26, null": "uncomfortable"
        }
    }
    mocker.patch('src.weather_analysis.UTCICalculator._load_categories', return_value=categories)

def test_utci_calculator(weather_data):
    calculator = UTCICalculator(weather_data)
    result = calculator.calculate()

    assert 'utci' in result
    assert 'stress_category' in result
    assert 'comfort_rating' in result
    assert result['stress_category'] == "extreme cold stress"
    assert result['comfort_rating'] == "very uncomfortable"
