from abc import ABC, abstractmethod
from weather_data import WeatherData
import utci_optimised
import numpy as np


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

    def calculate(self):
        """
        Calculates the Universal Thermal Climate Index (UTCI) based on the provided WeatherData.
        """
        eh_pa = self._exponential(self.weather_data.dry_bulb_temp) * (self.weather_data.relative_humidity / 100.0)
        delta_t_tr = self.weather_data.radiant_temp - self.weather_data.dry_bulb_temp
        pa = eh_pa / 10.0  # Convert vapour pressure to kPa
        
        utci_approx = utci_optimised.calc(self.weather_data.dry_bulb_temp, self.weather_data.wind_speed, delta_t_tr, pa)
        
        output = {'utci': np.round_(utci_approx, 5).tolist()}

        return output

    def _exponential(self, t_db):
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