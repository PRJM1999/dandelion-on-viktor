from dataclasses import dataclass
from ladybug.datacollection import HourlyContinuousCollection
import pandas as pd
import numpy as np

@dataclass
class WeatherData:
    """
    Class for keeping track of weather data necessary for UTCI calculation using hourly data collections.
    """
    dry_bulb_temp: HourlyContinuousCollection
    radiant_temp: HourlyContinuousCollection
    wind_speed: HourlyContinuousCollection
    wind_direction: HourlyContinuousCollection
    relative_humidity: HourlyContinuousCollection
    total_sky_cover: HourlyContinuousCollection
    units: str = "SI"

    def __post_init__(self):
        if self.units.lower() == "ip":
            self.convert_to_si()

    def convert_to_si(self):
        # Use built-in Ladybug methods to convert all relevant weather data to SI units
        self.dry_bulb_temp = self.dry_bulb_temp.convert_to_si()
        self.radiant_temp = self.radiant_temp.convert_to_si()
        self.wind_speed = self.wind_speed.convert_to_si()
        self.wind_direction = self.wind_speed.convert_to_si()
        self.relative_humidity = self.relative_humidity.convert_to_si()
        self.total_sky_cover = self.total_sky_cover.convert_to_si()
        self.units = "SI"

    def convert_to_ip(self):
        # Convert all relevant weather data to Imperial units if needed
        self.dry_bulb_temp = self.dry_bulb_temp.convert_to_ip()
        self.radiant_temp = self.radiant_temp.convert_to_ip()
        self.wind_speed = self.wind_speed.convert_to_ip()
        self.wind_direction = self.wind_speed.convert_to_ip()
        self.relative_humidity = self.relative_humidity.convert_to_ip()
        self.total_sky_cover = self.total_sky_cover.convert_to_ip()
        self.units = "IP"
    
    def get_wind_stats(self):
        """
        Generates wind statistics by categorizing wind directions into bins and calculating
        the frequency and average wind speed for each bin.

        Returns
        pandas.DataFrame
            A DataFrame with columns:
            - 'Wind Direction Bin': Categorical bins of wind direction (e.g., 'N', 'NE', 'E', etc.).
            - 'Frequency': The count of data points within each wind direction bin.
            - 'Average_Speed': The average wind speed (in the same units as input) for each bin.

        This function is currently part of a dataclass but should be refactored into its own
        behavior-focused class.
        """
        wind_df = pd.DataFrame({
            'Datetime': self.wind_direction.datetimes,
            'Wind Direction': self.wind_direction.values,
            'Wind Speed': self.wind_speed.values
        })

        direction_labels = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        wind_df['Wind Direction Bin'] = pd.cut(wind_df['Wind Direction'], bins=np.linspace(0, 360, num=17, endpoint=True), labels=direction_labels, right=False)

        stats_df = wind_df.groupby('Wind Direction Bin').agg(Frequency=('Wind Direction', 'size'), Average_Speed=('Wind Speed', 'mean')).reset_index()

        return stats_df

