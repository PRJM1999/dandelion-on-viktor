import pytest
from unittest.mock import patch, MagicMock
from src.station_retrieval import MongoEpwStorage

@pytest.fixture
def mock_mongo_client(mocker):
    # Setup the patch on the MongoClient at the package level where it is imported
    with patch('pymongo.MongoClient') as mock_client:
        mock_db = mock_client.return_value.__getitem__.return_value
        mock_collection = mock_db.__getitem__.return_value
        # Mocking find to return an iterator of dicts as MongoDB would
        mock_cursor = MagicMock()
        mock_cursor.__iter__.return_value = iter([
            {'lat': 34.05, 'lng': -118.25, 'name': 'Los Angeles'},  # Example document
            {'lat': 40.71, 'lng': -74.00, 'name': 'New York'}      # Example document
        ])
        mock_collection.find.return_value = mock_cursor
        yield mock_collection  # Using yield to ensure teardown happens after test completion

@pytest.fixture
def storage(mock_mongo_client):
    # Instantiate the storage with the mocked collection
    storage = MongoEpwStorage()
    storage.collection = mock_mongo_client  # Manually inject the mocked collection
    return storage

def test_fetch_closest_station(storage):
    # Test the function fetch_closest_station
    closest_station = storage.fetch_closest_station(34.05, -118.25)
    assert closest_station['name'] == 'Los Angeles'

def test_fetch_range_stations(storage):
    # Test the function fetch_range_stations
    stations_in_range = storage.fetch_range_stations(34.05, -118.25, 4000)
    assert len(stations_in_range) == 2
    assert set(station['name'] for station in stations_in_range) == {'Los Angeles', 'New York'}
