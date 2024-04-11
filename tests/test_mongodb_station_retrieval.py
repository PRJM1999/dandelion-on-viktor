import pytest
from station_retrieval import MongoEpwStorage
from unittest.mock import patch

# Keep the example documents and fixtures as before
example_documents = [
    {"_id": "1", "name": "Station1", "lat": 60.0, "lng": 20.0, "url": "http://example.com/station1.zip"},
    {"_id": "2", "name": "Station2", "lat": 61.0, "lng": 21.0, "url": "http://example.com/station2.zip"},
]

@pytest.fixture
def mock_mongo_collection():
    with patch('pymongo.collection.Collection.find') as mock_find:
        mock_find.return_value = example_documents  # Return our example documents when 'find' is called
        yield mock_find
        
@pytest.fixture
def storage(mock_mongo_collection):  # Include the mock here to ensure it's applied
    # This fixture now just needs to instantiate MongoEpwStorage
    return MongoEpwStorage()

def test_fetch_closest_station(storage):
    # Assuming a latitude and longitude that would make "Station1" the closest
    lat, lng = 60.01, 20.01
    result = storage.fetch_closest_station(lat, lng)
    assert result is not None  # We expect one result
    assert result['_id'] == "1"  # And that result should be the closest station

def test_fetch_range_stations(storage):
    # Test fetching stations within a 150km radius
    lat, lng = 60.01, 20.01
    radius = 150  # 150 kilometers
    result = storage.fetch_range_stations(lat, lng, radius)
    assert len(result) >= 1  # Assuming our mock data has at least one station within 150km
    assert any(doc['_id'] == "1" for doc in result)  # Check that "Station1" is included in the results
