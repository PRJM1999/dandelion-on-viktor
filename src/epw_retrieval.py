from abc import ABC, abstractmethod
from typing import List
from pymongo import MongoClient
from utility import haversine

class EpwRetrievalMethod(ABC):
    """
    Method to retreve relevant EPW file
    """

    @abstractmethod
    def fetch_by_coords(self, lat: float, lng: float) -> object:
        """
        Fetches the closet EPW data based upon global coordinates.

        Parameters:
        - lat (float): WGS84 Lattitude.
        - lng (float): WGS84 Longitude.

        Returns:
        - object: EPW weather data 
        """
        pass


class MongoEpwStorage(EpwRetrievalMethod):
    """
    Retrieves EPW file from internal AtkinsRealis database.
    """

    def __init__(self):
        self.client = MongoClient( 'mongodb://adminhcd:rD%5ETXq%407i7Bn@52.151.65.152:27017/admin?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')
        self.db = self.client['dandelion']
        self.collection = self.db['epw']
    
    def fetch_by_coords(self, lat: float, lng: float, closest: bool = True, radius: float = None) -> List[dict]:
        documents = self.collection.find({})
        distances = []

        for doc in documents:
            distance = haversine(lng, lat, doc['lng'], doc['lat'])
            if closest:
                distances.append((doc, distance))
            elif radius is not None and distance <= radius:
                distances.append((doc, distance))

        if closest:
            # Find the document with the minimum distance
            closest_doc = min(distances, key=lambda x: x[1])[0] if distances else None
            return [closest_doc] if closest_doc else []
        else:
            # Return all documents within the specified radius
            return [doc for doc, _ in distances]


