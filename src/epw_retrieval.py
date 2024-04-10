from abc import ABC, abstractmethod
from typing import List

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
    
    def fetch_by_coords(self, lat: float, lng: float) -> object:
        return super().fetch_by_coords(lat, lng)
