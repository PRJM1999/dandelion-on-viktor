from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from pymongo import MongoClient

from src.utility import haversine


class WeatherStationRetrieval(ABC):
    """
    Abstract base class to retrieve relevant EPW file.
    """

    @abstractmethod
    def fetch_closest_station(self, lat: float, lng: float) -> Optional[Dict]:
        """
        Fetches the closest EPW stations based upon global coordinates.

        Parameters:
        - lat (float): WGS84 Latitude.
        - lng (float): WGS84 Longitude.

        Returns:
        - Dict: Weather Station Data, or None if no station is found.
        """
        pass

    @abstractmethod
    def fetch_range_stations(self, lat: float, lng: float, radius: float) -> List[Dict]:
        """
        Fetches the EPW stations within a radial displacement of global coordinates.

        Parameters:
        - lat (float): WGS84 Latitude.
        - lng (float): WGS84 Longitude.
        - radius (float): Radial displacement in km.

        Returns:
        - List[Dict]: List containing weather stations.
        """
        pass


class MongoEpwStorage(WeatherStationRetrieval):
    """
    Retrieves EPW file from internal database.
    """

    def __init__(self):
        self.client = MongoClient('mongodb://adminhcd:rD%5ETXq%407i7Bn@52.151.65.152:27017/admin?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')
        self.db = self.client['dandelion']
        self.collection = self.db['epw']

    def fetch_closest_station(self, lat: float, lng: float) -> Optional[Dict]:
        documents = self.collection.find({})
        distances = [(doc, haversine(lng, lat, doc['lng'], doc['lat'])) for doc in documents]
        closest_doc = min(distances, key=lambda x: x[1])[0] if distances else None
        return closest_doc

    def fetch_range_stations(self, lat: float, lng: float, radius: float = 10) -> List[Dict]:
        documents = self.collection.find({})
        return [doc for doc in documents if haversine(lng, lat, doc['lng'], doc['lat']) <= radius]