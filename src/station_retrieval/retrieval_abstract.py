from abc import ABC, abstractmethod
from typing import List, Dict, Optional

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