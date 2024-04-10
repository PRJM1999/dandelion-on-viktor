from abc import ABC, abstractmethod
from weather_data import WeatherData
import utci_optimised
import numpy as np
import json


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

class UTCICalculator(WeatherAnalysis):
    def __init__(self, weather_data):
        super().__init__(weather_data)
        self.categories = self._load_categories("categories.json")
    
    @staticmethod
    def _load_categories(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def calculate(self):
        eh_pa = self._exponential(self.weather_data.dry_bulb_temp) * (self.weather_data.relative_humidity / 100.0)
        delta_t_tr = self.weather_data.radiant_temp - self.weather_data.dry_bulb_temp
        pa = eh_pa / 10.0
        
        utci_approx = utci_optimised.calc(self.weather_data.dry_bulb_temp, self.weather_data.wind_speed, delta_t_tr, pa)
        
        output = {'utci': np.round_(utci_approx, 5).tolist()}

        output['stress_category'] = self._get_category(utci_approx, self.categories['STRESS_CATEGORIES'])
        output['comfort_rating'] = self._get_category(utci_approx, self.categories['COMFORT_RATINGS'])

        return output

    def _get_category(self, utci_value: float, category_dict: dict) -> str:
        """
        Determines the category of the given UTCI value based on predefined bounds.

        Parameters:
        - utci_value (float): The Universal Thermal Climate Index value to categorize.
        - category_dict (dict): A dictionary mapping string bounds to category labels.

        Returns:
        - str: The category label if a matching range is found; "unknown" otherwise.

        """
        for key, category in category_dict.items():
            bounds = key.split(', ')
            lower = float(bounds[0]) if bounds[0] != "null" else None
            upper = float(bounds[1]) if bounds[1] != "null" else None

            if (lower is None or utci_value > lower) and (upper is None or utci_value <= upper):
                return category
        return "unknown"

    def _exponential(self, t_db: float) -> float:
        """
        Calculates the saturation vapor pressure (es) of air at a given 
        temperature using an adjusted Magnus-Tetens approximation.

        Parameters:
        - t_db (float): The dry-bulb temperature in degrees Celsius.

        Returns:
        - es (float): The saturation vapor pressure in hectoPascals (hPa), which indicates the maximum amount of water vapor 
                    that air can hold at the specified temperature.
        """
        
        g = [
            -2836.5744,
            -6028.076559,
            19.54263612,
            -0.02737830188,
            0.000016261698,
            (7.0229056 * np.power(10.0, -10)),
            (-1.8680009 * np.power(10.0, -13)),
        ]
        tk = t_db + 273.15  # air temp in K
        es = 2.7150305 * np.log1p(tk)
        for count, i in enumerate(g):
            es = es + (i * np.power(tk, count - 2))
        es = np.exp(es) * 0.01  # convert Pa to hPa
        return es

weather_data = WeatherData(dry_bulb_temp=25, radiant_temp=30, wind_speed=1.5, relative_humidity=50, units="SI")
calculator = UTCICalculator(weather_data=weather_data)
result = calculator.calculate(return_stress_category=True, return_comfort_rating=True)

print(result)