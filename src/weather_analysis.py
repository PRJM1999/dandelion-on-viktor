from src.utility import utci_optimised
from src.data_objects import WeatherData
import numpy as np
import json


class UTCICalculator():

    def __init__(self, weather_data: WeatherData):
        self.weather_data = weather_data
        self.categories = self._load_categories("src/categories.json")

    def calculate(self):
        eh_pa, delta_t_tr, pa = self._calculate_environmental_factors()
        
        utci_approx = utci_optimised(self.weather_data.dry_bulb_temp.average, self.weather_data.wind_speed.average, delta_t_tr, pa)
        
        output = {'utci': np.round_(utci_approx, 5).tolist()}

        output['stress_category'] = self._get_category(utci_approx, self.categories['STRESS_CATEGORIES'])
        output['comfort_rating'] = self._get_category(utci_approx, self.categories['COMFORT_RATINGS'])

        return output
    
    @staticmethod
    def _load_categories(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

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

    def _calculate_environmental_factors(self):
        """"
        Calculates the environmental factors needed for UTCI calculation.

        Returns:
        - eh_pa (float): Partial vapor pressure in hPa.
        - delta_t_tr (float): Difference between radiant temperature and dry bulb temperature.
        - pa (float): Modified partial vapor pressure used in UTCI calculation.
        """
        eh_pa = self._exponential(self.weather_data.dry_bulb_temp.average) * (self.weather_data.relative_humidity.average / 100.0)
        delta_t_tr = self.weather_data.radiant_temp.average - self.weather_data.dry_bulb_temp.average
        pa = eh_pa / 10.0
        return eh_pa, delta_t_tr, pa

    @staticmethod
    def _exponential(t_db: float) -> float:
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
        tk = t_db + 273.15 
        es = 2.7150305 * np.log1p(tk)
        for count, i in enumerate(g):
            es = es + (i * np.power(tk, count - 2))
        es = np.exp(es) * 0.01 
        return es