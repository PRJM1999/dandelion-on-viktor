from abc import ABC, abstractmethod
from .weather_data import WeatherData


class WeatherAnalysis(ABC):
    """
    Weather Analysis abstract class
    """

    def __init__(self, weather_data: WeatherData):
        self.weather_data = weather_data
    
    @abstractmethod
    def calculate(self):
        """
        Perform the specific weather analysis calculation.
        
        Must be implemented by subclasses.
        """
        pass