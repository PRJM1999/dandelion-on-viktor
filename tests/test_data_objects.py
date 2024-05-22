import pytest
from unittest.mock import Mock, create_autospec
from src.data_objects import WeatherData, SpeckleProject  
from ladybug.datacollection import HourlyContinuousCollection


@pytest.fixture
def hourly_data(mocker):
    collection = create_autospec(HourlyContinuousCollection)
    collection.convert_to_si.return_value = collection
    collection.convert_to_ip.return_value = collection
    return collection


def test_post_init_si_units(hourly_data):
    data = WeatherData(
        dry_bulb_temp=hourly_data,
        radiant_temp=hourly_data,
        wind_speed=hourly_data,
        wind_direction=hourly_data,
        relative_humidity=hourly_data,
        total_sky_cover=hourly_data,
        units="SI"
    )
    hourly_data.convert_to_si.assert_not_called()  


def test_post_init_ip_units(hourly_data):
    data = WeatherData(
        dry_bulb_temp=hourly_data,
        radiant_temp=hourly_data,
        wind_speed=hourly_data,
        wind_direction=hourly_data,
        relative_humidity=hourly_data,
        total_sky_cover=hourly_data,
        units="IP"
    )
    # Check if convert_to_si is called for each data collection
    assert hourly_data.convert_to_si.call_count == 6, "convert_to_si should be called for each attribute"


def test_convert_to_si(hourly_data):
    # Initialize the WeatherData instance with "IP" units, which triggers automatic conversion to "SI"
    data = WeatherData(
        dry_bulb_temp=hourly_data,
        radiant_temp=hourly_data,
        wind_speed=hourly_data,
        wind_direction=hourly_data,
        relative_humidity=hourly_data,
        total_sky_cover=hourly_data,
        units="IP"
    )
    # Reset mock call counts after automatic conversion in __post_init__
    hourly_data.convert_to_si.reset_mock()

    # Explicitly call convert_to_si method to test this functionality alone
    data.convert_to_si()

    # Assert that convert_to_si is called exactly once for each attribute after method call
    assert hourly_data.convert_to_si.call_count == 6, "convert_to_si should be called for each attribute after method call"


def test_convert_to_ip(hourly_data):
    # Test explicit call to convert_to_ip method
    data = WeatherData(
        dry_bulb_temp=hourly_data,
        radiant_temp=hourly_data,
        wind_speed=hourly_data,
        wind_direction=hourly_data,
        relative_humidity=hourly_data,
        total_sky_cover=hourly_data,
    )
    # Reset mock call counts after automatic conversion in __post_init__
    hourly_data.convert_to_si.reset_mock()

    data.convert_to_ip()
    assert hourly_data.convert_to_ip.call_count == 6, "convert_to_ip should be called for each attribute after method call"


def test_speckle_project_initialization():
    stream_id = "12345"
    name = "Example Project"
    lat = 40.7128
    long = -74.0060

    project = SpeckleProject(stream_id=stream_id, name=name, lat=lat, long=long)

    assert project.stream_id == stream_id
    assert project.name == name
    assert project.lat == lat
    assert project.long == long

    # Test default values
    default_project = SpeckleProject(stream_id=stream_id, name=name)
    assert default_project.lat is None
    assert default_project.long is None