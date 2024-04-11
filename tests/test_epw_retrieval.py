import pytest
from src.epw_retrieval import MongoEpwStorage 
from src.utility import haversine
from unittest.mock import patch, MagicMock

# Example documents that might exist in your MongoDB collection
example_documents = [
    {"_id": "1", "name": "Station1", "lat": 60.0, "lng": 20.0},
    {"_id": "2", "name": "Station2", "lat": 61.0, "lng": 21.0},
]

@pytest.fixture
def mock_mongo_collection():
    with patch('pymongo.collection.Collection.find') as mock_find:
        mock_find.return_value = example_documents  # Return our example documents when 'find' is called
        yield mock_find
        
@pytest.fixture
def storage(mock_mongo_collection):  # Include the mock here to ensure it's applied
    # Assuming MongoClient is correctly mocked within MongoEpwStorage if necessary
    # This fixture now just needs to instantiate MongoEpwStorage
    return MongoEpwStorage()

@pytest.fixture
def test_fetch_by_coords_closest(storage, mock_mongo_collection):
    # Assuming a latitude and longitude that would make "Station1" the closest
    lat, lng = 60.01, 20.01
    result = storage.fetch_by_coords(lat, lng, closest=True)
    assert len(result) == 1  # We expect one result
    assert result[0]['_id'] == "1"  # And that result should be the closest station

def test_fetch_by_coords_within_radius(storage, mock_mongo_collection):
    # Test fetching stations within a 150km radius
    lat, lng = 60.01, 20.01
    radius = 150000  # 150 kilometers in meters
    result = storage.fetch_by_coords(lat, lng, closest=False, radius=radius)
    assert len(result) > 1  # Assuming our mock data has more than one station within 150km
    assert any(doc['_id'] == "1" for doc in result)  # Check that "Station1" is included in the results

